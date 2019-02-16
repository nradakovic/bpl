#!/usr/bin/env python3
# --------------------------------------------------------------
# logger.py
# --------------------------------------------------------------
# Copyright (C) 2019 Nikola Radakovic
# email: radaknikolans@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

""" Logger module for writhing messages to standard output
"""

# --------------------------------------------------------------
# Imports
# --------------------------------------------------------------
import sys
import inspect
# --------------------------------------------------------------
# Global variables & classes
# --------------------------------------------------------------


class Colors:
    """
    Log class for color output
    """

    RED = '\033[31m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'
    DARK_YELLOW = '\033[33m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    RESET = '\033[39m'

    OFF = int(0)
    ON = int(1)


class Log:
    """
    Log class for output
    """
    ERROR = int(1)
    WARNING = int(2)
    INFO = int(4)
    DEBUG = int(8)
    DEBUG_2 = int(16)
    DEBUG_3 = int(32)
    ENTER_EXIT_POINT = int(64)
    ALL = int(127)

    def __init__(self, log_level=0, enable_color=Colors.OFF, default_offset=50):
        """ Constructor for logger module
        :param log_level: Log level of the instance
        :param enable_color: If 1 use colorized output, otherwise no
        :param default_offset: Used to determent the offset base
        """
        self.__log_level = log_level
        self.__enable_color = enable_color
        self.__header = ""
        self.__default_offset = default_offset
        self.__enable_header = False

    def __get_color(self, color):
        """ Check if the color output is enabled or not
        :param color: requested color
        :return: if colorized output is enabled, requested @param::color will be
                 returned, otherwise default color console output is used.
        """
        if self.__enable_color:
            return color
        return Colors.RESET

    def __construct_header(self, data):
        """ Construct a header as prefix to log message by inspecting stack
        :param data: call sequence stack
        :return: Constructed header based on stack inspection
        """
        if data[1][3] == '<module>':
            call_function = 'main'
        else:
            call_function = data[1][3]
        line = str(data[1][2])
        self.__header = f'[{call_function}::{line}]'

    def __print_log_with_header(self, offset, print_color, label, msg):
        """ Print function with header as prefix
        :param offset:
        :param print_color:
        :param label:
        :param msg:
        :return:
        """
        print('{}{}{}{}{}: {}'.format(self.__header,
                                      "".ljust(offset),
                                      self.__get_color(print_color),
                                      label,
                                      Colors.RESET,
                                      msg))

    def __print_log(self, print_color, label, label_offset, msg):
        """ [PRIVATE]: Print function without header as prefix
        :param print_color:
        :param label:
        :param label_offset:
        :param msg:
        :return:
        """
        print('{}{}{}{}{}{}'.format(self.__get_color(print_color),
                                    label,
                                    Colors.RESET,
                                    label_offset,
                                    "".ljust(5),
                                    msg))

    def set_log_level(self, level, color):
        """ Set the log level
        :param level: Level to be set
        :param color: Color to be set
        """
        self.__log_level = level
        self.__enable_color = color

    def append_log_level(self, level):
        """ Append the new log level to the current one
        :param level: Log level to be append
        """
        self.__log_level |= level

    def remove_log_level(self, level):
        """ Remove log level from current setup
        :param level: Log level to be removed
        """
        self.__log_level &= (~level)

    def get_log_level(self):
        """ Return current log level
        :return: Current log level
        """
        return self.__log_level

    def enable_log_color(self, enable):
        """ Turn OFF/ON the color output
        :param enable: If 1 enable color output, else default color output
        """
        self.__enable_color = enable

    def enable_header(self, enable):
        """ Turn ON/OFF header prefix
        :param enable: If True header prefix will be added to the log
        """
        self.__enable_header = enable

    def i(self, message):
        """ Info log
        :param message: Text to be printed on this level
        """
        if (self.__log_level & self.INFO) > 0:
            if self.__enable_header:
                self.__construct_header(inspect.stack())
                offset = self.__default_offset - len(self.__header)\
                    - 4 - len("INFO")
                self.__print_log_with_header(offset,
                                             Colors.GREEN,
                                             "INFO",
                                             message)
            else:
                self.__print_log(Colors.GREEN, "INFO", ":    ", message)

    def w(self, message):
        """ Warning log
        :param message: Text to be printed on this level
        """
        if (self.__log_level & self.WARNING) > 0:
            if self.__enable_header:
                self.__construct_header(inspect.stack())
                offset = self.__default_offset - len(self.__header) - 4 - len("WARNING")
                self.__print_log_with_header(offset, Colors.YELLOW, "WARNING", message)
            else:
                self.__print_log(Colors.YELLOW, "WARNING", ": ", message)

    def e(self, message):
        """ Error log
        :param message: Text to be printed on this level
        """
        if(self.__log_level & self.ERROR) > 0:
            if self.__enable_header:
                self.__construct_header(inspect.stack())
                offset = self.__default_offset - len(self.__header) - 4 - len("ERROR")
                self.__print_log_with_header(offset, Colors.RED, "ERROR", message)
            else:
                self.__print_log(Colors.RED, "ERROR", ":   ", message)

    def d(self, message):
        """ Debug log - level 1
        :param message: Text to be printed on this level
        """
        if(self.__log_level & self.DEBUG) > 0:
            if self.__enable_header:
                self.__construct_header(inspect.stack())
                offset = self.__default_offset - len(self.__header) - 4 - len("DEBUG")
                self.__print_log_with_header(offset, Colors.BLUE, "DEBUG", message)
            else:
                self.__print_log(Colors.BLUE, "DEBUG", ":   ", message)

    def d2(self, message):
        """ Debug log - level 2
        :param message: Text to be printed on this level
        """
        if(self.__log_level & self.DEBUG_2) > 0:
            if self.__enable_header:
                self.__construct_header(inspect.stack())
                offset = self.__default_offset - len(self.__header) - 4 - len("DEBUG_2")
                self.__print_log_with_header(offset, Colors.CYAN, "DEBUG_2", message)
            else:
                self.__print_log(Colors.CYAN, "DEBUG_2", ": ", message)

    def d3(self, message):
        """ Debug log - level 3
        :param message: Text to be printed on this level
        """
        if(self.__log_level & self.DEBUG_3) > 0:
            if self.__enable_header:
                self.__construct_header(inspect.stack())
                offset = self.__default_offset - len(self.__header) - 4 - len("DEBUG_3")
                self.__print_log_with_header(offset, Colors.PURPLE, "DEBUG_3", message)
            else:
                self.__print_log(Colors.PURPLE, "DEBUG_3", ": ", message)

    def enter(self, name=""):
        """ Debug log - for logging function name on entry point
        :param name: Class name
        """
        if(self.__log_level & self.ENTER_EXIT_POINT) > 0:
            self.__construct_header(inspect.stack())
            message = ""
            if self.__enable_header:
                offset = self.__default_offset - len(self.__header) - 4 - len("_ENTER_")
                if name != "":
                    message = "<" + Colors.PURPLE + "class" + Colors.RESET \
                                 + ": " + Colors.BLUE + name + Colors.RESET + ">"
                    self.__print_log_with_header(offset, Colors.PURPLE, "_ENTER_", message)
            else:
                class_name = ""
                if name != "":
                    class_name = " [" + Colors.BLUE + name + Colors.RESET + "]"
                message = ">>> " + self.__get_color(Colors.YELLOW) + self.__header + Colors.RESET + class_name
                self.__print_log(Colors.PURPLE, "ENTER", ":   ", message)

    def exit(self, name=""):
        """ Debug log - for logging function name on exit point
        :param name: Class name
        """
        if(self.__log_level & self.ENTER_EXIT_POINT) > 0:
            self.__construct_header(inspect.stack())
            message = ""
            if self.__enable_header:
                offset = self.__default_offset - len(self.__header) - 4 - len("_EXIT_")
                if name != "":
                    message = "<" + Colors.PURPLE + "class" + Colors.RESET \
                                 + ": " + Colors.BLUE + name + Colors.RESET + ">"
                    self.__print_log_with_header(offset, Colors.PURPLE, "_EXIT_", message)
            else:
                class_name = ""
                if name != "":
                    class_name = " [" + Colors.BLUE + name + Colors.RESET + "]"
                message = "<<< " + self.__get_color(Colors.YELLOW) + self.__header + Colors.RESET + class_name
                self.__print_log(Colors.PURPLE, "EXIT", ":    ", message)

    def no_header(self, log_level, message):
        """ Log without header which will be written based on current log level of instance
        :param log_level: statically set log level
        :param message: Text to be printed on this level
        """
        if (self.__log_level & log_level) > 0:
            print(message)


# ====================================================
# Main loop - This is only for testing this script
# ====================================================
if __name__ == '__main__':

    sys.dont_write_bytecode = True

    log = Log(Log.INFO | Log.ERROR, Colors.ON)

    # ---------- TEST 1 -----------
    # Enabling only INFO and ERROR logs
    log.set_log_level(Log.INFO | Log.ERROR, Colors.ON)
    test = "1"

    log.i("This" +
          " is a test " + test)
    log.w("This is a test " + test)
    log.e("This is a test " + test)
    log.d("This is a test " + test)
    log.d2("This is a test " + test)
    log.d3("This is a test " + test)
    log.enter()
    log.exit()

    # ---------- TEST 2 --------
    # Enabling ALL logs
    log.append_log_level(Log.ALL)
    test = "2"

    log.i("This" +
          " is a test " + test)
    log.w("This is a test " + test)
    log.e("This is a test " + test)
    log.d("This is a test " + test)
    log.d2("This is a test " + test)
    log.d3("This is a test " + test)
    log.enter("TestClass")
    log.exit("TestClass")

    # ---------- TEST 3 --------
    # Disabling DEBUG_3 and ENTER_EXIT logs
    log.remove_log_level(Log.DEBUG_3 | Log.ENTER_EXIT_POINT)
    test = "3"

    log.i("This" +
          " is a test " + test)
    log.w("This is a test " + test)
    log.e("This is a test " + test)
    log.d("This is a test " + test)
    log.d2("This is a test " + test)
    log.d3("This is a test " + test)
    log.enter("TestClass")
    log.exit("TestClass")

    # ---------- TEST 4 --------
    # Disabling DEBUG_4 and ENTER_EXIT logs
    log.set_log_level(Log.ALL, Colors.ON)
    log.enable_header(True)
    test = "4"

    log.i("This" +
          " is a test " + test)
    log.w("This is a test " + test)
    log.e("This is a test " + test)
    log.d("This is a test " + test)
    log.d2("This is a test " + test)
    log.d3("This is a test " + test)
    log.enter("TestClass")
    log.exit("TestClass")