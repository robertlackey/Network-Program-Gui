class ssh:
    client = None

    def __init__(self, address, username, password):
        # Let the user know we're connecting to the device
        print("Connecting to device")
            # Create a new SSH client
        self.client = paramiko.SSHClient()
            # The following line is required if you want the script to be able to access a devices that's not yet in the known_hosts file
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Make the connection
        self.client.connect(address, username=username, password=password, look_for_keys=False)

    def sendCommand(self, command):
        #time.sleep(20)
        chan = self.client.invoke_shell()
        chan.send(command)
        print("sending commands")
        clientbuffer = []
        try:
            while not chan.exit_status_ready():
                if chan.recv_ready():
                    data = chan.recv(9999)
                    while data:
                        clientbuffer.append(data)
                        data = chan.recv(9999)
            self.clientoutput = ''.join(clientbuffer)
        except:
            raise
        print(self.clientoutput)
        self.client.close()
        sys.stdout = StdoutRedirect(self.clientoutput)
