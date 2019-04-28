
from netmon.network import Network
from os import system, name
from ctypes import *

from multiprocessing.dummy import Pool as ThreadPool
import threading
from itertools import product
import datetime

from threading import Lock

import cursor
cursor.hide()

#-------- <windows only>---------------

from dependency.win import color_console as Colors

STD_OUTPUT_HANDLE = -11

class COORD(Structure):
    pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]
#-------- </windows only>---------------

class Printer:
    mutex = Lock()
    current_row = 0

    COLOR_DEFAULT = Colors.get_text_attr()
    COLOR_DEFAULT_BG = COLOR_DEFAULT & 0x0070

    @staticmethod
    def set_printer_color_to_red():
        Colors.set_text_attr(Colors.FOREGROUND_RED | Printer.COLOR_DEFAULT_BG )

    @staticmethod
    def set_printer_color_to_default():
        Colors.set_text_attr(Printer.COLOR_DEFAULT | Printer.COLOR_DEFAULT_BG )
        # Colors.set_text_attr(Colors.FOREGROUND_GREY | Printer.color_default_bg )

    def __init__(self, thread_count = 4):
        self.thread_count = thread_count

    def __del__(self):
        cursor.show()

    @staticmethod
    def print_at(r, c, s, addNewLine=1):

        if r is 0:
            r = Printer.current_row
        #-------- <windows only>---------------
        h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
        c = s.encode("windows-1252")
        windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
        #-------- </windows only>---------------

        Printer.current_row = r + addNewLine


    @staticmethod
    def print_at_tuple(print_at_args):
        Printer.mutex.acquire()

        r, c, s, addNewLine, isup = print_at_args
        if not isup:
            Printer.set_printer_color_to_red()
        Printer.print_at(r, c, s, addNewLine)
        Printer.set_printer_color_to_default()

        Printer.mutex.release()

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
    def format_other(message, message2='', max_len = 78):
        just_lenth = max_len
        final_message  = '|'
        if message2 != '':
            just_lenth = int(max_len/2)
            final_message += message2.ljust(just_lenth)
        final_message += message.rjust(just_lenth)
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
                isup_status = 'up' if Network.Addresses[key].Is_Up else 'down !'
                to_print = Printer.format_line(
                        key,
                        Network.Addresses[key].Ip,
                        isup_status,
                        datetime.timedelta(seconds=Network.Addresses[key].Uptime),
                        datetime.timedelta(seconds=Network.Addresses[key].Downtime)
                    )

                print_queue.append((index, 0, to_print, 1, Network.Addresses[key].Is_Up))
                printer_thread_pool.map(Printer.print_at_tuple, print_queue)

        printer_thread_pool.close()
        printer_thread_pool.join()

