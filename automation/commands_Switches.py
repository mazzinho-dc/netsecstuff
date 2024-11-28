import paramiko
import time
import getpass  # To securely get the password from the user

def read_ip_addresses(filename):
    """Reads a list of IP addresses from a file."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]  # Remove empty lines

def send_command(ssh, command):
    """Send a single command to the SSH session."""
    ssh.send(command + '\n')
    time.sleep(1)
    output = ssh.recv(65535).decode('utf-8')
    return output

def configure_switch(ip, username, password, commands):
    """Function to SSH into the switch and run configuration commands."""
    try:
        # Create an SSH client instance
        ssh_client = paramiko.SSHClient()

        # Automatically add the remote host key (if missing) to known hosts
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the switch using SSH
        print(f"Connecting to {ip}...")
        ssh_client.connect(hostname=ip, username=username, password=password)

        # Open an interactive shell session
        ssh = ssh_client.invoke_shell()
        time.sleep(1)

        # Read any initial output
        ssh.recv(65535)

        # Send commands to enter privileged EXEC mode
        print("Entering enable mode...")
        ssh.send('enable\n')
        time.sleep(1)
        ssh.send(password + '\n')  # Enter the password again if prompted for enable mode
        time.sleep(1)

        # Send commands to enter global configuration mode
        print("Entering configuration mode...")
        ssh.send('configure terminal\n')
        time.sleep(1)
        
        # Send each configuration command
        for command in commands:
            print(f"Sending command: {command}")
            ssh.send(command + '\n')
            time.sleep(1)

        # Exit configuration mode and close the SSH connection
        ssh.send('end\n')
        time.sleep(1)
        ssh.send('write memory\n')  # Save the configuration
        time.sleep(1)
        
        output = ssh.recv(65535).decode('utf-8')
        print(f"Configuration output for {ip}:")
        print(output)

        # Close the connection
        ssh_client.close()
        print(f"Configuration on {ip} completed successfully.")

    except paramiko.AuthenticationException:
        print(f"Authentication failed for {ip}, please check your credentials.")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection to {ip}: {sshException}")
    except Exception as e:
        print(f"Error occurred on {ip}: {str(e)}")

if __name__ == "__main__":
    # File containing the list of switch IPs
    ip_file = "switch_ips.txt"

    # Read the IP addresses from the file
    switches = read_ip_addresses(ip_file)

    # Prompt for device credentials
    username = input("Enter your SSH username: ")
    password = getpass.getpass("Enter your SSH password: ")

    # Commands to configure on all switches
    commands_list = [
        "logging buffered 16384",
        "end",
        "wr",
        "exit"
        
    ]

    # Iterate over the list of switches and configure each one
    for switch_ip in switches:
        print(f"\nConfiguring switch {switch_ip}...")
        configure_switch(switch_ip, username, password, commands_list)
