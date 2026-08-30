from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.186.129",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5000,
}


# ============================================================
# SW1 CONFIGURATION COMMANDS
# ============================================================

commands = [

    # --------------------------------------------------------
    # 1. Set SW1 hostname
    # --------------------------------------------------------

    "hostname SW1",


    # --------------------------------------------------------
    # 2. Create VLAN 63 - Warehouse
    # --------------------------------------------------------

    "vlan 63",
    "name WAREHOUSE",
    "exit",


    # --------------------------------------------------------
    # 3. Create VLAN 73 - Management
    # --------------------------------------------------------

    "vlan 73",
    "name MANAGEMENT",
    "exit",


    # --------------------------------------------------------
    # 4. Configure Gi0/0
    # Link between SW1 and R1
    # --------------------------------------------------------

    "interface GigabitEthernet0/0",
    "description TRUNK_TO_R1",
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan 63,73",
    "no shutdown",
    "exit",


    # --------------------------------------------------------
    # 5. Configure Gi0/1
    # Warehouse terminal
    # --------------------------------------------------------

    "interface GigabitEthernet0/1",
    "description WAREHOUSE_TERMINAL",
    "switchport mode access",
    "switchport access vlan 63",
    "no shutdown",
    "exit",


    # --------------------------------------------------------
    # 6. Configure Gi0/2
    # Management terminal
    # --------------------------------------------------------

    "interface GigabitEthernet0/2",
    "description MANAGEMENT_TERMINAL",
    "switchport mode access",
    "switchport access vlan 73",
    "no shutdown",
    "exit",


    "end",
]


# ============================================================
# CONNECT AND CONFIGURE SW1
# ============================================================

connection = None

try:

    print("=" * 65)
    print("Connecting to SW1...")
    print("=" * 65)

    connection = ConnectHandler(**switch)

    print("Connected to SW1 successfully.")

    # --------------------------------------------------------
    # Check current prompt
    # --------------------------------------------------------

    print("\nCurrent SW1 prompt:")

    print(connection.find_prompt())


    # --------------------------------------------------------
    # Enter privileged EXEC mode
    # --------------------------------------------------------

    print("\nEntering privileged EXEC mode...")

    if not connection.check_enable_mode():

        connection.enable()

    print("Privileged EXEC mode entered successfully.")


    # --------------------------------------------------------
    # Send configuration commands
    # --------------------------------------------------------

    print("\nApplying SW1 configuration...")

    output = connection.send_config_set(
        commands
    )

    print(output)


    # --------------------------------------------------------
    # Save configuration
    # --------------------------------------------------------

    print("\nSaving SW1 configuration...")

    connection.save_config()

    print("\n" + "=" * 65)
    print("SW1 CONFIGURATION COMPLETED SUCCESSFULLY")
    print("=" * 65)


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
        f"\nUnexpected error while configuring SW1: "
        f"{error}"
    )


finally:

    if connection is not None:

        connection.disconnect()

        print("\nDisconnected from SW1.")
        