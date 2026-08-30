from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# ============================================================
# R1 CONNECTION DETAILS
# ============================================================

router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.186.129",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5002,       # R1 GNS3 TELNET port
}


# ============================================================
# R1 VERIFICATION COMMANDS
# ============================================================

verification_commands = [

    # --------------------------------------------------------
    # 1. Verify interface status and IP addresses
    # --------------------------------------------------------

    "show ip interface brief",


    # --------------------------------------------------------
    # 2. Verify R1 routing table
    # --------------------------------------------------------

    "show ip route",


    # --------------------------------------------------------
    # 3. Verify OSPF configuration and process
    # --------------------------------------------------------

    "show ip protocols",


    # --------------------------------------------------------
    # 4. Verify OSPF neighbors
    # R2 should appear as an OSPF neighbor.
    # --------------------------------------------------------

    "show ip ospf neighbor",


    # --------------------------------------------------------
    # 5. Verify routes learned through OSPF
    # Site-B networks should appear here.
    # --------------------------------------------------------

    "show ip route ospf",


    # --------------------------------------------------------
    # 6. Verify OSPF interface information
    # --------------------------------------------------------

    "show ip ospf interface brief",
]


# ============================================================
# CONNECT AND VERIFY R1
# ============================================================

connection = None

try:

    print("=" * 65)
    print("Connecting to R1...")
    print("=" * 65)

    connection = ConnectHandler(**router)

    print("Connected to R1 successfully.")


    # --------------------------------------------------------
    # Enter privileged EXEC mode
    # --------------------------------------------------------

    if router["secret"]:

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
    print("R1 VERIFICATION COMPLETED")
    print("=" * 65)


# ============================================================
# ERROR HANDLING
# ============================================================

except NetmikoTimeoutException:

    print(
        "\nConnection timed out.\n"
        "Check the GNS3 VM IP address, R1 TELNET console "
        "port, GNS3 VM, and R1 state."
    )


except NetmikoAuthenticationException:

    print(
        "\nAuthentication failed.\n"
        "Check the username, password, and enable password."
    )


except Exception as error:

    print(
        f"\nUnexpected error while verifying R1: "
        f"{error}"
    )


# ============================================================
# CLOSE CONNECTION
# ============================================================

finally:

    if connection is not None:

        connection.disconnect()

        print("\nDisconnected from R1.")