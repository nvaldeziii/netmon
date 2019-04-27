import os
import time

from multiprocessing.dummy import Pool as ThreadPool
import threading

class Network:
    def __init__(self, thread_count = 4):
        self.Addresses = {}
        self.Count = 0
        self.ping_all_execution_time = 0
        self.thread_count = thread_count

    def __del__(self):
        pass

    def add_ip_address(self, name, IpObj, forced = False):
        if name in self.Addresses and not forced:
            raise self.DuplicateAddressExceptionError('Duplicate Network Name was found!')

        self.Addresses[name] = IpObj
        self.Count = self.Count + 1

    def ping_all(self):
        start = time.time()
        network_thread_pool = ThreadPool(self.thread_count)
        network_thread_pool.map(self.ping_address, list(self.Addresses.keys()))
        network_thread_pool.close()
        network_thread_pool.join()

        self.ping_all_execution_time = time.time() - start

    def ping_address(self, key):
        self.Addresses[key].refresh(Network.ping_ip(self.Addresses[key].Ip), int(time.time()))

    @staticmethod
    def ping_ip(ip):
        return True if os.system('ping -n 1 -w 1 ' + ip + ' > nul') is 0 else False

    class DuplicateAddressExceptionError(Exception):
        """Raised if duplicate name has been added to the network"""
        pass

if __name__ == '__main__':
    pass