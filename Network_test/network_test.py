from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# ============================================================
# DEVICE CONNECTION DETAILS
# ============================================================

devices = [

    {
        "name": "R1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.186.129",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5002,       # R1 GNS3 TELNET port
    },

    {
        "name": "R2",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.186.129",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5004,       # R2 GNS3 TELNET port
    },
]


# ============================================================
# WHOLE NETWORK TESTS
# ============================================================

testing_commands = [

    # ========================================================
    # R1 TESTS
    # ========================================================

    [
        "R1",

        # ----------------------------------------------------
        # 1. Test R1 -> R2
        # ----------------------------------------------------

        "ping 10.18.18.2",


        # ----------------------------------------------------
        # 2. Test R1 -> Site-A Warehouse gateway
        # ----------------------------------------------------

        "ping 172.26.63.1",


        # ----------------------------------------------------
        # 3. Test R1 -> Site-A Management gateway
        # ----------------------------------------------------

        "ping 172.26.73.1",


        # ----------------------------------------------------
        # 4. Test R1 -> Site-B Warehouse gateway
        # ----------------------------------------------------

        "ping 172.27.63.1",


        # ----------------------------------------------------
        # 5. Test R1 -> Site-B Management gateway
        # ----------------------------------------------------

        "ping 172.27.73.1",


        # ----------------------------------------------------
        # 6. Verify OSPF neighbor
        # ----------------------------------------------------

        "show ip ospf neighbor",


        # ----------------------------------------------------
        # 7. Verify OSPF routes
        # ----------------------------------------------------

        "show ip route ospf",


        # ----------------------------------------------------
        # 8. Verify complete routing table
        # ----------------------------------------------------

        "show ip route",
    ],


    # ========================================================
    # R2 TESTS
    # ========================================================

    [
        "R2",

        # ----------------------------------------------------
        # 1. Test R2 -> R1
        # ----------------------------------------------------

        "ping 10.18.18.1",


        # ----------------------------------------------------
        # 2. Test R2 -> Site-B Warehouse gateway
        # ----------------------------------------------------

        "ping 172.27.63.1",


        # ----------------------------------------------------
        # 3. Test R2 -> Site-B Management gateway
        # ----------------------------------------------------

        "ping 172.27.73.1",


        # ----------------------------------------------------
        # 4. Test R2 -> Site-A Warehouse gateway
        # ----------------------------------------------------

        "ping 172.26.63.1",


        # ----------------------------------------------------
        # 5. Test R2 -> Site-A Management gateway
        # ----------------------------------------------------

        "ping 172.26.73.1",


        # ----------------------------------------------------
        # 6. Verify OSPF neighbor
        # ----------------------------------------------------

        "show ip ospf neighbor",


        # ----------------------------------------------------
        # 7. Verify OSPF routes
        # ----------------------------------------------------

        "show ip route ospf",


        # ----------------------------------------------------
        # 8. Verify complete routing table
        # ----------------------------------------------------

        "show ip route",
    ],
]


# ============================================================
# CONNECT TO EACH DEVICE AND RUN TESTS
# ============================================================

for device in devices:

    connection = None

    device_name = device["name"]


    # --------------------------------------------------------
    # Remove the name field because Netmiko does not use it.
    # --------------------------------------------------------

    connection_details = {
        key: value
        for key, value in device.items()
        if key != "name"
    }


    # --------------------------------------------------------
    # Find the tests assigned to this device.
    # --------------------------------------------------------

    commands_for_device = []

    for command_group in testing_commands:

        if command_group[0] == device_name:

            commands_for_device = command_group[1:]

            break


    if not commands_for_device:

        print(
            f"\n{device_name}: "
            "No network tests have been assigned."
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
        # Enter privileged EXEC mode
        # ----------------------------------------------------

        if connection_details["secret"]:

            connection.enable()


        # ====================================================
        # RUN TESTS
        # ====================================================

        for command in commands_for_device:

            print("\n" + "-" * 65)

            print(
                f"{device_name}: Testing {command}"
            )

            print("-" * 65)


            output = connection.send_command(
                command,
                read_timeout=30,
            )


            print(output)


        print(
            f"\n{device_name} testing completed."
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except NetmikoTimeoutException:

        print(
            f"\n{device_name}: Connection timed out.\n"
            "Check that the device is running in GNS3, "
            "verify the GNS3 server IP address, "
            "and verify the TELNET console port."
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
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 65)
print("WHOLE NETWORK TESTING COMPLETED")
print("=" * 65)