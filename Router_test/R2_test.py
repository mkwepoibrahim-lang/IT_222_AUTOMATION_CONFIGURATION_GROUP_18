from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# ============================================================
# R2 CONNECTION DETAILS
# ============================================================

router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.186.129",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5004,       # R2 GNS3 TELNET port
}


# ============================================================
# R2 NETWORK TESTS
# ============================================================

testing_commands = [

    # --------------------------------------------------------
    # 1. Test R2 -> R1
    # R1 Gi0/0 = 10.18.18.1
    # --------------------------------------------------------

    "ping 10.18.18.1",


    # --------------------------------------------------------
    # 2. Test R2 VLAN 63 gateway
    # --------------------------------------------------------

    "ping 172.27.63.1",


    # --------------------------------------------------------
    # 3. Test R2 VLAN 73 gateway
    # --------------------------------------------------------

    "ping 172.27.73.1",


    # --------------------------------------------------------
    # 4. Test connectivity to Site-A Warehouse network
    # R1 VLAN 63 gateway = 172.26.63.1
    # --------------------------------------------------------

    "ping 172.26.63.1",


    # --------------------------------------------------------
    # 5. Test connectivity to Site-A Management network
    # R1 VLAN 73 gateway = 172.26.73.1
    # --------------------------------------------------------

    "ping 172.26.73.1",


    # --------------------------------------------------------
    # 6. Check OSPF neighbors
    # --------------------------------------------------------

    "show ip ospf neighbor",


    # --------------------------------------------------------
    # 7. Check OSPF-learned routes
    # --------------------------------------------------------

    "show ip route ospf",


    # --------------------------------------------------------
    # 8. Check complete routing table
    # --------------------------------------------------------

    "show ip route",
]


# ============================================================
# CONNECT AND TEST R2
# ============================================================

connection = None

try:

    print("=" * 65)
    print("Connecting to R2...")
    print("=" * 65)

    connection = ConnectHandler(**router)

    print("Connected to R2 successfully.")


    # --------------------------------------------------------
    # Enter privileged EXEC mode
    # --------------------------------------------------------

    if router["secret"]:

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
    print("R2 NETWORK TESTING COMPLETED")
    print("=" * 65)


# ============================================================
# ERROR HANDLING
# ============================================================

except NetmikoTimeoutException:

    print(
        "\nConnection timed out.\n"
        "Check that R2 is running in GNS3 and "
        "verify the GNS3 VM IP address and TELNET port."
    )


except NetmikoAuthenticationException:

    print(
        "\nAuthentication failed.\n"
        "Check the username, password, and enable password."
    )


except Exception as error:

    print(
        f"\nUnexpected error while testing R2: "
        f"{error}"
    )


# ============================================================
# CLOSE CONNECTION
# ============================================================

finally:

    if connection is not None:

        connection.disconnect()

        print("\nDisconnected from R2.")