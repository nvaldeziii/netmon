
from netmon.network import Network
from os import system, name
from ctypes import *

from multiprocessing.dummy import Pool as ThreadPool
import threading
from itertools import product

from threading import Lock

import cursor
cursor.hide()

#-------- <windows only>---------------
STD_OUTPUT_HANDLE = -11

class COORD(Structure):
    pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]
#-------- </windows only>---------------

class Printer:
    mutex = Lock()
    current_row = 0

    def __init__(self, thread_count = 4):
        self.thread_count = thread_count

    def __del__(self):
        cursor.show()

    @staticmethod
    def print_at(r, c, s, addNewLine=1):
        Printer.mutex.acquire()
        if r is 0:
            r = Printer.current_row
        #-------- <windows only>---------------
        h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
        c = s.encode("windows-1252")
        windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
        #-------- </windows only>---------------

        Printer.current_row = r + addNewLine
        Printer.mutex.release()

    @staticmethod
    def print_at_tuple(print_at_args):
        r, c, s, addNewLine = print_at_args
        Printer.print_at(r, c, s, addNewLine)

    @staticmethod
    def format_header(message, max_len = 76):
        final_message = '|'
        FIRST_HALF_LEN = int((max_len - len(message)) / 2)
        for i in range(0, FIRST_HALF_LEN):
            final_message += '_'
        final_message += '| ' + message + '|'
        for i in range(0, FIRST_HALF_LEN):
            final_message += '_'
        final_message += '|'

        Printer.print_at(0,0,final_message)

    @staticmethod
    def format_top(max_len = 80):
        message = Printer.format_line('Name','Ip Address','Status','Uptime','Downtime')
        Printer.print_at(0,0, message)

    @staticmethod
    def format_bar(max_len = 80):
        message = "|"
        for i in range(0, max_len - 2):
            message += '-'
        message += '|'
        Printer.print_at(0,0, message)

    @staticmethod
    def format_line(name, ip, stat, up, down):
        message  = '| {}| {}| {}| {}| {}|'.format(
            name.ljust(11), ip.ljust(17),stat.ljust(13), str(up).ljust(13), str(down).ljust(15)
        )
        return message

    @staticmethod
    def format_other(message, max_len = 78):
        final_message  = '|'
        final_message += message.rjust(max_len)
        final_message += '|'
        Printer.print_at(0 ,0, final_message)

    def print(self, Network):
        Printer.current_row = 0
        Printer.format_header('Network Monitoring Tool')
        Printer.format_top()
        Printer.format_bar()
        print_queue = []
        printer_thread_pool = ThreadPool(self.thread_count)
        for index, key in enumerate(sorted(Network.Addresses), start=Printer.current_row):
                to_print = Printer.format_line(key, Network.Addresses[key].Ip, str(Network.Addresses[key].Is_Up),
                    Network.Addresses[key].Uptime, Network.Addresses[key].Downtime)

                print_queue.append((index, 0, to_print, 1))
                printer_thread_pool.map(Printer.print_at_tuple, print_queue)

        printer_thread_pool.close()
        printer_thread_pool.join()

