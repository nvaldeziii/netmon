
from netmon.network import Network
from os import system, name
from ctypes import *

from multiprocessing.dummy import Pool as ThreadPool
import threading
from itertools import product

from threading import Lock

STD_OUTPUT_HANDLE = -11

class COORD(Structure):
    pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]

class Printer:
    def __init__(self, thread_count = 4):
        self.thread_count = thread_count

    mutex = Lock()
    current_row = 0
    @staticmethod
    def print_at(r, c, s, addNewLine=1):
        Printer.mutex.acquire()
        h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))

        c = s.encode("windows-1252")
        windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
        Printer.current_row = r + addNewLine
        Printer.mutex.release()

    @staticmethod
    def print_at_tuple(print_at_args):
        r, c, s, addNewLine = print_at_args
        Printer.print_at(r, c, s, addNewLine)

    def print(self, Network):
        Printer.print_at(0,0,"==================== Network Monitoring Tool ====================")
        print_queue = []
        printer_thread_pool = ThreadPool(self.thread_count)
        for index, key in enumerate(sorted(Network.Addresses), start=Printer.current_row):
                to_print = '{} -> {} | isup: {} | uptime: {} | downtime: {}'.format(
                    key ,Network.Addresses[key].Ip ,str(Network.Addresses[key].Is_Up)
                    ,Network.Addresses[key].Uptime ,Network.Addresses[key].Downtime
                )
                print_queue.append((index, 0, to_print, 1))

                # Printer.print_at(index, 0, to_print)

                printer_thread_pool.map(Printer.print_at_tuple, print_queue)
        printer_thread_pool.close()
        printer_thread_pool.join()

