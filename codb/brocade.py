
import re
from time import sleep

from paramiko import SSHClient, AutoAddPolicy


class SwitchStack:

    def __init__(self, name, ip, username, password, port=22):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.switches = None
        self.vlans = None
        self.connected = False

    ######################################################################
    # Switch connection methods
    ######################################################################

    def __connect(self):
        print("Connecting to %s at %s" % (self.name, self.ip))
        self.__client = SSHClient()
        self.__client.set_missing_host_key_policy(AutoAddPolicy())
        self.__client.connect(self.ip, username=self.username, password=self.password, port=self.port)
        self.__shell = self.__client.invoke_shell()
        self.__prompt = self.__shell.recv(1000)
        self.connected = True

    def __close(self):
        print("Closing connection to %s" % self.ip)
        self.connected = False
        self.__shell.close()
        self.__client.close()

    def __execute(self, command):
        if not self.connected:
            raise Exception ("Not connected yet!")

        # Make sure we end with a newline
        if not command.endswith('\n'):
            command += '\n'

        # Send the command
        self.__shell.send(command)
        sleep(0.1)

        # Receive the response
        response = b''
        while self.__shell.recv_ready():
            r = self.__shell.recv(1000)
            if b'\x08' in r:
                r = r.replace(b'\x08', b'')
                # r = r.strip()
            response +=  r
        return response.decode("ascii")

    def __pull_switches(self):
        self.switches = {}
        stack_data = self.__execute("show stack")
        recording = False
        for line in stack_data.splitlines():
            if not recording:
                if line.startswith("ID"):
                    recording = True
                continue
            else:
                if line == "":
                    recording = False
                    break
                switch_data = line.split(" ")
                switch_name = self.name + '-' + switch_data[0]
                self.switches[switch_name] = {
                    'ID': switch_data[0],
                    'Type': switch_data[3],
                    'Role': switch_data[6],
                    'Mac': switch_data[8],
                }

    def __pull_vlans(self):
        # Gather our vlan data
        vlan_data = self.__execute("show vlans")
        while vlan_data.endswith("next page: Space, next line: Return key, quit: Control-c"):
            vlan_data += '\n' + self.__execute(' ')

        # Process our vlan data
        vlan_id = None
        for line in vlan_data.splitlines():
            new_vlan = line.strip().startswith("PORT-VLAN")
            if new_vlan:
                vlan_id = line.strip().split(" ")[1][:-1]
            elif vlan_id:
                # Only read lines with one of these: (U1/M1)
                # where the module equals: 1
                if '(' in line and line[22] == '1':
                    switch_name = self.name + '-' + line[19]
                    switch = self.switches[switch_name]
                    ports = ' '.join(line[26:].split())
                    if not 'VLANS' in switch:
                        switch['VLANS'] = {}
                    if not 'PORTS' in switch:
                        switch['PORTS'] = {}
                    # print(f'Switch: {switch_name}, VLAN: {vlan_id}, Ports: {ports}')
                    for port in ports.split():
                        port_number = int(port)
                        if not vlan_id in switch['VLANS']:
                            switch['VLANS'][vlan_id] = {'Untagged': [], 'Tagged': []}
                        if not port_number in switch['PORTS']:
                            switch['PORTS'][port_number] = {'Untagged': [], 'Tagged': []}
                        if line[1] == 'U':
                            switch['PORTS'][port_number]['Untagged'].append(vlan_id)
                            switch['VLANS'][vlan_id]['Untagged'].append(port_number)
                        elif line[3] == 'T':
                            switch['PORTS'][port_number]['Tagged'].append(vlan_id)
                            switch['VLANS'][vlan_id]['Tagged'].append(port_number)

    def __pull_data(self):
        self.__connect()
        self.__pull_switches()
        self.__pull_vlans()
        self.__close()

    ######################################################################
    # User methods
    ######################################################################

    def print_stack(self):
        if not self.switches:
            self.__pull_data()

        for switch_name in self.switches.keys():
            switch = self.switches[switch_name]
            port_numbers = switch['PORTS'].keys()
            for port in sorted(port_numbers):
                vlans = switch['PORTS'][port]
                print(f"{switch_name} {port}: {vlans}")
