import os
import time
import datetime
import sys
sys.path.insert(0, '..')
from netmon.file_reader import FileReader
from netmon.network import Network
from netmon.ip_address import IpAddress
from netmon.printer import Printer

class Netmon:
    def __init__(self, IpFile):
        self.Network = Network()
        self.Printer = Printer()
        IpListFile = FileReader(IpFile)
        for line in IpListFile.Lines:
            self.Network.add_ip_address(line.name,IpAddress(line.ip))

    def run_continuously(self):
        os.system('cls')
        while(True):
            start = time.time()
            self.run()
            Printer.format_bar()
            Printer.format_other('     total probe time: {}s'.format(str(round(self.Network.ping_all_execution_time, 4)))
                , str(datetime.datetime.now()))
            total_proc_time = time.time() - start
            Printer.format_other('total processing time: {}s'.format(str(round(total_proc_time,4))))
            Printer.format_bar()
            time.sleep(1 - total_proc_time)

    def run(self):
            self.Network.ping_all()
            self.Printer.print(self.Network)

def main():
    NetmonProgram = Netmon('ipaddress.json')
    NetmonProgram.run_continuously()

if __name__ == "__main__":
    main()


