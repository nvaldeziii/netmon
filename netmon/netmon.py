import os
import time
import datetime
import sys
sys.path.insert(0, '..')
from netmon.file_reader import FileReader
from netmon.network import Network
from netmon.printer import Printer

class IpAddress:
    def __init__(self, value, initial_time=int(time.time())):
        self.Ip = value
        self.Uptime = 0
        self.Downtime = 0
        self.time_of_last_success_ping = initial_time
        self.time_of_last_ping = initial_time
        self.Is_Up = True
        self.downtime_count = 0
        self.time_before_false_negative = initial_time

    def is_major_downtime(self):
        return self.downtime_count > 2

    def ping_ok(self, time_of_last_ping):
        if not self.Is_Up:
            if self.is_major_downtime():
                self.time_of_last_success_ping = time_of_last_ping
                self.downtime_count = 0
            else:
                self.time_of_last_success_ping = self.time_before_false_negative
        self.time_before_false_negative = self.time_of_last_success_ping
        self.refresh_uptime(time_of_last_ping)

    def ping_not_ok(self, time_of_last_ping):
        if self.Is_Up:
            self.time_of_last_success_ping = self.time_of_last_ping
        if self.is_major_downtime():
            self.refresh_downtime(time_of_last_ping)
        else:
            self.downtime_count += 1

    def refresh(self, current_ping_status, time_of_last_ping):
        if current_ping_status:
            self.ping_ok(time_of_last_ping)
        else:
            self.ping_not_ok(time_of_last_ping)

        self.time_of_last_ping = time_of_last_ping
        self.Is_Up = current_ping_status

    def time_delta_from_last_ping(self, time_of_last_ping):
        return time_of_last_ping - self.time_of_last_success_ping

    def refresh_uptime(self, time_of_last_ping):
        self.Uptime = self.time_delta_from_last_ping(time_of_last_ping)

    def refresh_downtime(self, time_of_last_ping):
        self.Downtime = self.time_delta_from_last_ping(time_of_last_ping)

class Netmon:
    def __init__(self, IpFile):
        self.Network = Network()
        self.Printer = Printer()
        IpListFile = FileReader(IpFile)
        for line in IpListFile.Lines:
            raw = line.split(',')
            self.Network.add_ip_address(raw[0].strip(),IpAddress(raw[1].strip()))

    def Run_Continuously(self):
        os.system('cls')
        while(True):
            start = time.time()
            self.Run()
            Printer.format_bar()
            Printer.format_other('     total probe time: {}s'.format(str(round(self.Network.ping_all_execution_time, 4)))
                , str(datetime.datetime.now()))
            total_proc_time = time.time() - start
            Printer.format_other('total processing time: {}s'.format(str(round(total_proc_time,4))))
            Printer.format_bar()
            time.sleep(1 - total_proc_time)

    def Run(self):
            self.Network.ping_all()
            self.Printer.print(self.Network)

def main():
    NetmonProgram = Netmon('ipaddress.txt')
    NetmonProgram.Run_Continuously()

if __name__ == "__main__":
    main()


