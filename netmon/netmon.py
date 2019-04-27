import re
import os
import time

class IpAddress:
    def __init__(self, value, initial_time=int(time.time())):
        self.Ip = value
        self.Uptime = 0
        self.Downtime = 0
        self.time_of_last_success_ping = initial_time
        self.time_of_last_ping = initial_time
        self.Is_Up = False

    def refresh(self, current_ping_status, time_of_last_ping):
        if current_ping_status:
            self.refresh_uptime(time_of_last_ping)
        else:
            if not current_ping_status and self.Is_Up:
                self.time_of_last_success_ping = self.time_of_last_ping
            self.refresh_downtime(time_of_last_ping)

        self.time_of_last_ping = time_of_last_ping
        self.Is_Up = current_ping_status

    def time_delta_from_last_ping(self, time_of_last_ping):
        return time_of_last_ping - self.time_of_last_success_ping

    def refresh_uptime(self, time_of_last_ping):
        self.Uptime = self.time_delta_from_last_ping(time_of_last_ping)

    def refresh_downtime(self, time_of_last_ping):
        self.Downtime = self.time_delta_from_last_ping(time_of_last_ping)

class Network:
    def __init__(self):
        self.Addresses = {}
        self.Count = 0

    def add_ip_address(self, name, IpObj, forced = False):
        if name in self.Addresses and not forced:
            raise self.DuplicateAddressExceptionError('Duplicate Network Name was found!')

        self.Addresses[name] = IpObj
        self.Count = self.Count + 1

    def ping_all(self):
        for key in sorted(self.Addresses):
            isup = self.ping(self.Addresses[key].Ip)
            self.Addresses[key].refresh(isup, int(time.time()))

    def ping(self, ip):
        return True if os.system('ping -n 1 -w 1 ' + ip + ' > nul') is 0 else False

    class DuplicateAddressExceptionError(Exception):
        """Raised if duplicate name has been added to the network"""
        pass

class Printer:
    def __init__(self):
        pass

    def print(self, Network):
        for key in sorted(Network.Addresses):
                to_print = '{} -> {} | isup: {} | uptime: {} | downtime: {}'.format(
                    key ,Network.Addresses[key].Ip ,str(Network.Addresses[key].Is_Up)
                    ,Network.Addresses[key].Uptime ,Network.Addresses[key].Downtime
                )
                print(to_print)

class FileReader:
    def __init__(self,filename):
        self.IpFile = open(filename, 'r')
        self.Lines = []
        self.read()

    def read(self):
        for linestring in self.IpFile:
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
            self.Network.ping_all()
            self.Printer.print(self.Network)


NetmonProgram = Netmon('ipaddress.txt')
NetmonProgram.Run_Continuously()
