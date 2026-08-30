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
# SW1 NETWORK TESTS
# ============================================================

testing_commands = [

    # --------------------------------------------------------
    # 1. Check learned MAC addresses
    # --------------------------------------------------------

    "show mac address-table",


    # --------------------------------------------------------
    # 2. Check VLAN configuration
    # VLAN 63 = Warehouse
    # VLAN 73 = Management
    # --------------------------------------------------------

    "show vlan brief",


    # --------------------------------------------------------
    # 3. Check trunk configuration
    # Gi0/0 should be trunking toward R1.
    # --------------------------------------------------------

    "show interfaces trunk",


    # --------------------------------------------------------
    # 4. Check interface status
    # --------------------------------------------------------

    "show ip interface brief",


    # --------------------------------------------------------
    # 5. Check Gi0/0 trunk interface
    # --------------------------------------------------------

    "show interfaces GigabitEthernet0/0",


    # --------------------------------------------------------
    # 6. Check Gi0/1 Warehouse access port
    # --------------------------------------------------------

    "show interfaces GigabitEthernet0/1",


    # --------------------------------------------------------
    # 7. Check Gi0/2 Management access port
    # --------------------------------------------------------

    "show interfaces GigabitEthernet0/2",
]


# ============================================================
# CONNECT AND TEST SW1
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
    # Run each network test
    # --------------------------------------------------------

    for command in testing_commands:

        print("\n" + "-" * 65)
        print(f"Testing: {command}")
        print("-" * 65)

        output = connection.send_command(
            command,
            read_timeout=30
        )

        print(output)


    print("\n" + "=" * 65)
    print("SW1 NETWORK TESTING COMPLETED")
    print("=" * 65)


# ============================================================
# ERROR HANDLING
# ============================================================

except NetmikoTimeoutException:

    print(
        "\nConnection timed out.\n"
        "Check that SW1 is running in GNS3 and "
        "verify the GNS3 VM IP address and TELNET port."
    )


except NetmikoAuthenticationException:

    print(
        "\nAuthentication failed.\n"
        "Check the username, password, and enable password."
    )


except Exception as error:

    print(
        f"\nUnexpected error while testing SW1: "
        f"{error}"
    )


# ============================================================
# CLOSE CONNECTION
# ============================================================

finally:

    if connection is not None:

        connection.disconnect()

        print("\nDisconnected from SW1.")