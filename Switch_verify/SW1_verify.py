from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# ============================================================
# SW1 CONNECTION DETAILS
# ============================================================

switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.186.129",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5000,       # SW1 GNS3 TELNET port
}


# ============================================================
# SW1 VERIFICATION COMMANDS
# ============================================================

verification_commands = [

    # --------------------------------------------------------
    # 1. Verify VLAN configuration
    # VLAN 63 = Warehouse
    # VLAN 73 = Management
    # --------------------------------------------------------

    "show vlan brief",


    # --------------------------------------------------------
    # 2. Verify interface status
    # --------------------------------------------------------

    "show interfaces status",


    # --------------------------------------------------------
    # 3. Verify IP interface information
    # --------------------------------------------------------

    "show ip interface brief",


    # --------------------------------------------------------
    # 4. Verify trunk configuration
    # Gi0/0 should be trunking toward R1.
    # --------------------------------------------------------

    "show interfaces trunk",


    # --------------------------------------------------------
    # 5. Verify MAC address table
    # --------------------------------------------------------

    "show mac address-table",
]


# ============================================================
# CONNECT AND VERIFY SW1
# ============================================================

connection = None

try:

    print("=" * 65)
    print("Connecting to SW1...")
    print("=" * 65)

    connection = ConnectHandler(**switch)

    print("Connected to SW1 successfully.")


    # --------------------------------------------------------
    # Enter privileged EXEC mode
    # --------------------------------------------------------

    if switch["secret"]:

        connection.enable()


    # --------------------------------------------------------
    # Run each verification command
    # --------------------------------------------------------

    for command in verification_commands:

        print("\n" + "-" * 65)
        print(f"--- {command} ---")
        print("-" * 65)

        output = connection.send_command(
            command,
            read_timeout=30
        )

        print(output)


    print("\n" + "=" * 65)
    print("SW1 VERIFICATION COMPLETED")
    print("=" * 65)


# ============================================================
# ERROR HANDLING
# ============================================================

except NetmikoTimeoutException:

    print(
        "\nConnection timed out.\n"
        "Check the GNS3 VM IP address, SW1 TELNET console "
        "port, GNS3 VM, and SW1 state."
    )


except NetmikoAuthenticationException:

    print(
        "\nAuthentication failed.\n"
        "Check the username, password, and enable password."
    )


except Exception as error:

    print(
        f"\nUnexpected error while verifying SW1: "
        f"{error}"
    )


# ============================================================
# CLOSE CONNECTION
# ============================================================

finally:

    if connection is not None:

        connection.disconnect()

        print("\nDisconnected from SW1.")