from netmiko import ConnectHandler
import getpass
import json

def check_ip_(ip, username, password):
    try:
        with ConnectHandler(**switch) as conn:
            # the device is reachable
            return True
    except:
        return False

# Prompt for username and password
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

# Prompt for VLAN to add
vlanid = input("VLAN ID to add: ")
vlanname = input("Name for VLAN:")

# Load the switch connection parameters from the JSON file
with open("switches.json") as f:
    switches = json.load(f)

# Loop through each switch and configure the VLAN
for switch in switches:
    # Add the username and password to the switch parameters
    switch["username"] = username
    switch["password"] = password

    if check_ip_(switch["ip"], username, password):
        print(f'{switch["ip"]} is reachable')
        # Open an SSH connection to the switch
        with ConnectHandler(**switch) as conn:
            # Send commands to create the VLAN with a name attribute
            vlan_commands = [
                f"vlan {vlanid}",
                f"name {vlanname}",
                "end",
                "write",
            ]
            output = conn.send_config_set(vlan_commands)
            print(output)
    else:
        print(f'{switch["ip"]} is not reachable')
