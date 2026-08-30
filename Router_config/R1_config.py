from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)



router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.186.129",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5002,       # R1 GNS3 TELNET port
}


# ============================================================
# R1 CONFIGURATION COMMANDS
# ============================================================

commands = [

    # --------------------------------------------------------
    # 1. Set R1 hostname
    # --------------------------------------------------------

    "hostname R1",


    # --------------------------------------------------------
    # 2. Configure Gi0/0
    # Link between R1 and R2
    #
    # Network: 10.18.18.0/30
    # R1 IP:   10.18.18.1
    # --------------------------------------------------------

    "interface GigabitEthernet0/0",
    "description LINK_TO_R2",
    "ip address 10.18.18.1 255.255.255.252",
    "no shutdown",
    "exit",


    # --------------------------------------------------------
    # 3. Configure physical Gi0/1
    # Link between R1 and SW1
    #
    # This interface will carry VLAN 63 and VLAN 73.
    # --------------------------------------------------------

    "interface GigabitEthernet0/1",
    "description TRUNK_TO_SW1",
    "no shutdown",
    "exit",


    # --------------------------------------------------------
    # 4. Configure VLAN 63 Warehouse subinterface
    #
    # Network: 172.26.63.0/24
    # Gateway: 172.26.63.1
    # --------------------------------------------------------

    "interface GigabitEthernet0/1.63",
    "description VLAN_63_WAREHOUSE",
    "encapsulation dot1Q 63",
    "ip address 172.26.63.1 255.255.255.0",
    "no shutdown",
    "exit",


    # --------------------------------------------------------
    # 5. Configure VLAN 73 Management subinterface
    #
    # Network: 172.26.73.0/24
    # Gateway: 172.26.73.1
    # --------------------------------------------------------

    "interface GigabitEthernet0/1.73",
    "description VLAN_73_MANAGEMENT",
    "encapsulation dot1Q 73",
    "ip address 172.26.73.1 255.255.255.0",
    "no shutdown",
    "exit",


    # --------------------------------------------------------
    # 6. Configure OSPF
    # --------------------------------------------------------

    "router ospf 1",
    "router-id 1.1.1.1",

    # R1 <-> R2 network
    "network 10.18.18.0 0.0.0.3 area 0",

    # Site-A Warehouse network
    "network 172.26.63.0 0.0.0.255 area 0",

    # Site-A Management network
    "network 172.26.73.0 0.0.0.255 area 0",

    "end",
]


# ============================================================
# CONNECT AND CONFIGURE R1
# ============================================================

connection = None

try:

    print("=" * 65)
    print("Connecting to R1...")
    print("=" * 65)

    connection = ConnectHandler(**router)

    print("Connected to R1 successfully.")


    # Enter privileged EXEC mode if enable secret is configured
    if router["secret"]:
        connection.enable()


    # --------------------------------------------------------
    # Send configuration commands
    # --------------------------------------------------------

    print("\nApplying R1 configuration...")

    output = connection.send_config_set(
        commands
    )

    print(output)


    # --------------------------------------------------------
    # Save configuration
    # --------------------------------------------------------

    print("\nSaving R1 configuration...")

    connection.save_config()

    print("\n" + "=" * 65)
    print("R1 CONFIGURATION COMPLETED SUCCESSFULLY")
    print("=" * 65)


# ============================================================
# ERROR HANDLING
# ============================================================

except NetmikoTimeoutException:

    print(
        "\nConnection timed out.\n"
        "Check that R1 is running in GNS3 and "
        "verify the GNS3 VM IP address and TELNET port."
    )


except NetmikoAuthenticationException:

    print(
        "\nAuthentication failed.\n"
        "Check the username, password, and enable password."
    )


except Exception as error:

    print(
        f"\nUnexpected error while configuring R1: "
        f"{error}"
    )


# ============================================================
# CLOSE CONNECTION
# ============================================================

finally:

    if connection is not None:

        connection.disconnect()

        print("\nDisconnected from R1.")