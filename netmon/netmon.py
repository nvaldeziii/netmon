import re
import os
import time
import sys
sys.path.insert(0, '..')
from netmon.network import Network
from netmon.printer import Printer

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
        os.system('cls')
        while(True):
            start = time.time()
            self.Run()
            Printer.format_bar()
            Printer.format_other('probe time: {}s'.format(str(round(self.Network.ping_all_execution_time, 4))))
            Printer.format_other('total proc time: {}s'.format(str(round(time.time() - start,4))))
            Printer.format_bar()
            time.sleep(1)

    def Run(self):
            self.Network.ping_all()
            self.Printer.print(self.Network)

def main():
    NetmonProgram = Netmon('ipaddress.txt')
    NetmonProgram.Run_Continuously()

if __name__ == "__main__":
    main()


