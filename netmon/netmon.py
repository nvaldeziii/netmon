import re
import os
import time

class IpAddress:
    def __init__(self, value):
        self.Ip = value
        self.Uptime = 0
        self.Downtime = 0
        self.Time_last_success_ping = 0
        self.Is_Up = False

    def refresh(self):
        pass

class Network:
    def __init__(self):
        self.Address = {}
        self.Count = 0

    def add_ip_address(self, name, IpObj, forced = False):
        if name in self.Address and not forced:
            raise self.DuplicateAddressException('Duplicate Network Name was found!')

        self.Address[name] = IpObj
        self.Count = self.Count + 1

    def ping_all(self):
        for key in sorted(self.Address):
            self.ping(key)

    def ping(self, name):
        self.Address[name].Is_Up = True if os.system('ping -n 1 -w 1 ' + self.Address[name].Ip + ' > nul') is 0 else False
        return self.Address[name].Is_Up

    class DuplicateAddressException(Exception):
        """Raised if duplicate name has been added to the network"""
        pass

class Printer:
    def __init__(self):
        pass

    def print(self, Network):
        for key in sorted(Network.Address):
                print( key + ' -> ' + Network.Address[key].Ip + ' is ' + str(Network.Address[key].Is_Up))

class FileReader:
    def __init__(self,filename):
        self.IpFile = open(filename, 'r')
        self.Lines = []
        self.read()

    def read(self):
        for linenumber, linestring in enumerate(self.IpFile):
            if re.match(r'^[^#]\w+,\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',linestring.strip()):
                self.Lines.append(linestring.strip())

    def __del__(self):
        self.IpFile.close()

class Netmon:
    def __init__(self, IpFile):
        self.Network = Network()
        self.Printer = Printer()
        IpListFile = FileReader(IpFile)
        for line in IpListFile.Lines:
            raw = line.split(',')
            self.Network.add_ip_address(raw[0],IpAddress(raw[1]))

    def Run_Continuously(self):
        while(True):
            os.system('cls')
            self.Run()
            time.sleep(1)

    def Run(self):
            self.Printer.print(self.Network)
            self.Network.ping_all()


# NetmonProgram = Netmon('ipaddress.txt')
# NetmonProgram.Run_Continuously()
