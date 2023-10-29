from netmiko import ConnectHandler
import time

# Define the device parameters for SSH connection
ssh_device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'prne',
    'password': 'cisco123!',
    'secret': 'class123!', # Enable secret password
}

def ssh_menu():
    print("SSH Menu")
    print("1. Change Device Hostname")
    print("2. Save Running Configuration")
    print("3. Exit")
    
    choice = input("Enter your choice (1/2/3): ")
    
    if choice == "1":
        change_hostname()
    elif choice == "2":
        save_running_config()
    elif choice == "3":
        print("Exiting SSH Menu")
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        ssh_menu()

def change_hostname():
    new_hostname = input("Enter the new hostname: ")
    
    while True:
        try:
            ssh_conn = ConnectHandler(**ssh_device) # Corrected here
            ssh_conn.enable() # Enter enable mode
            ssh_conn.config_mode() # Enter global configuration mode
            ssh_conn.send_command('hostname ' + new_hostname)
            ssh_conn.exit_config_mode() # Exit configuration mode
            ssh_conn.send_command('write memory') # Save configuration
            ssh_conn.disconnect()
            break
        except ValueError as e:
            print(f"Error: {e}")
            print("Retrying...")
            time.sleep(5)
    
    print(f"Device hostname changed to {new_hostname}")

def save_running_config():
    while True:
        try:
            ssh_conn = ConnectHandler(**ssh_device) # Corrected here
            ssh_conn.enable() # Enter enable mode
            running_config = ssh_conn.send_command('show running-config') # Capture the output
            ssh_conn.disconnect()
            break
        except ValueError as e:
            print(f"Error: {e}")
            print("Retrying...")
            time.sleep(5)
    
    with open('running_config.txt', 'w') as f:
        f.write(running_config)
    
    print("Running configuration saved to running_config.txt")

if __name__ == "__main__":
    while True:
        ssh_menu()
