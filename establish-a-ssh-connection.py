import paramiko
ssh = paramiko.SSHClient()
ssh.start_client()

# Define the SSH connection parameters
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
new_hostname = 'R1'

# Create an SSH client object
ssh = paramiko.SSHClient()

# Automatically add the SSH server's host key (no need to do this in a real setting)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Try to establish a connection to the SSH server
try:
    ssh.connect(ip_address, username=username, password=password)
except paramiko.AuthenticationException:
    print('---FAILURE! Authentication failed, please verify your credentials')
    exit()
except paramiko.SSHException as sshException:
    print('---FAILURE! Unable to establish SSH connection: ', sshException)
    exit()
except paramiko.BadHostKeyException as badHostKeyException:
    print('---FAILURE! Unable to verify server\'s host key: ', badHostKeyException)
    exit()

# If the connection was successful, create a new channel for remote commands
channel = ssh.invoke_shell()

# Send the command to modify the device hostname
channel.send('configure terminal\n')
channel.send('hostname ' + new_hostname + '\n')
channel.send('end\n')

# Wait for the command to complete
while not channel.recv_ready():
    pass

# Print the output of the command
print(channel.recv(1024).decode('utf-8'))

# Close the SSH connection
ssh.close()

​


