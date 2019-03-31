import re

class IpAddress:
    def __init__(self, value):
        self.Ip = value
        self.uptime = 0
        self.downtime = 0
        self.time_last_success_ping = 0

    def refresh(self):
        pass

class Network:
    def __init__(self):
        self.Address = {}

    def add_ip_address(self, name, IpObj):
        self.Address[name] = IpObj

class Printer:
    def __init__(self, IpAddresses):
        pass

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
        IpListFile = FileReader(IpFile)
        for line in IpListFile.Lines:
            raw = line.split(',')
            self.Network.add_ip_address(raw[0],IpAddress(raw[1]))

    def Run(self):
        pass


NetmonProgram = Netmon('ipaddress.txt')
NetmonProgram.Run()