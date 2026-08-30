from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# ============================================================
# DEVICE CONNECTION DETAILS
# ============================================================

devices = [

    # --------------------------------------------------------
    # R1
    # --------------------------------------------------------

    {
        "name": "R1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.186.129",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5002,
    },


    # --------------------------------------------------------
    # R2
    # --------------------------------------------------------

    {
        "name": "R2",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.186.129",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5004,
    },


    # --------------------------------------------------------
    # SW1
    # --------------------------------------------------------

    {
        "name": "SW1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.186.129",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5000,
    },


    # --------------------------------------------------------
    # SW2
    # --------------------------------------------------------

    {
        "name": "SW2",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.186.129",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5006,
    },
]


# ============================================================
# NETWORK VERIFICATION COMMANDS
# ============================================================

verification_commands = [

    # ========================================================
    # R1 VERIFICATION
    # ========================================================

    [
        "R1",

        # Check R1 interfaces and IP addresses
        "show ip interface brief",

        # Check complete R1 routing table
        "show ip route",

        # Check OSPF configuration
        "show ip protocols",

        # Check OSPF neighbor relationship with R2
        "show ip ospf neighbor",

        # Check OSPF-learned Site-B routes
        "show ip route ospf",

        # Check OSPF interfaces
        "show ip ospf interface brief",
    ],


    # ========================================================
    # R2 VERIFICATION
    # ========================================================

    [
        "R2",

        # Check R2 interfaces and IP addresses
        "show ip interface brief",

        # Check complete R2 routing table
        "show ip route",

        # Check OSPF configuration
        "show ip protocols",

        # Check OSPF neighbor relationship with R1
        "show ip ospf neighbor",

        # Check OSPF-learned Site-A routes
        "show ip route ospf",

        # Check OSPF interfaces
        "show ip ospf interface brief",
    ],


    # ========================================================
    # SW1 VERIFICATION
    # ========================================================

    [
        "SW1",

        # Check VLAN 63 and VLAN 73
        "show vlan brief",

        # Check trunk between SW1 and R1
        "show interfaces trunk",

        # Check physical interface status
        "show interfaces status",

        # Check switch interface information
        "show ip interface brief",

        # Check learned MAC addresses
        "show mac address-table",
    ],


    # ========================================================
    # SW2 VERIFICATION
    # ========================================================

    [
        "SW2",

        # Check VLAN 63 and VLAN 73
        "show vlan brief",

        # Check trunk between SW2 and R2
        "show interfaces trunk",

        # Check physical interface status
        "show interfaces status",

        # Check switch interface information
        "show ip interface brief",

        # Check learned MAC addresses
        "show mac address-table",
    ],
]


# ============================================================
# CONNECT TO EACH DEVICE AND VERIFY
# ============================================================

for device in devices:

    connection = None

    device_name = device["name"]


    # --------------------------------------------------------
    # Remove device name because Netmiko does not use it.
    # --------------------------------------------------------

    connection_details = {
        key: value
        for key, value in device.items()
        if key != "name"
    }


    # --------------------------------------------------------
    # Find commands assigned to the current device.
    # --------------------------------------------------------

    commands_for_device = []

    for command_group in verification_commands:

        if command_group[0] == device_name:

            commands_for_device = command_group[1:]

            break


    # --------------------------------------------------------
    # Check whether commands exist.
    # --------------------------------------------------------

    if not commands_for_device:

        print(
            f"\n{device_name}: "
            "No verification commands have been assigned."
        )

        continue


    # ========================================================
    # CONNECT TO DEVICE
    # ========================================================

    try:

        print("\n" + "=" * 65)
        print(f"Connecting to {device_name}...")
        print("=" * 65)


        connection = ConnectHandler(
            **connection_details
        )


        print(
            f"Connected to {device_name} successfully."
        )


        # ----------------------------------------------------
        # Enter privileged EXEC mode if required.
        # ----------------------------------------------------

        if connection_details["secret"]:

            connection.enable()


        # ====================================================
        # RUN VERIFICATION COMMANDS
        # ====================================================

        for command in commands_for_device:

            print("\n" + "-" * 65)

            print(
                f"--- {device_name}: {command} ---"
            )

            print("-" * 65)


            output = connection.send_command(
                command,
                read_timeout=30
            )


            print(output)


        print(
            f"\n{device_name} verification completed."
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except NetmikoTimeoutException:

        print(
            f"\n{device_name}: Connection timed out.\n"
            "Check the GNS3 VM IP address, TELNET console "
            "port, GNS3 VM, and device state."
        )


    except NetmikoAuthenticationException:

        print(
            f"\n{device_name}: Authentication failed.\n"
            "Check the username, password, and enable password."
        )


    except Exception as error:

        print(
            f"\n{device_name}: "
            f"Unexpected error: {error}"
        )


    # ========================================================
    # CLOSE CONNECTION
    # ========================================================

    finally:

        if connection is not None:

            connection.disconnect()

            print(
                f"\nDisconnected from {device_name}."
            )


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 65)
print("WHOLE NETWORK VERIFICATION COMPLETED")
print("=" * 65)