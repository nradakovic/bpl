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

__version__ = "0.2.0"
__author__ = "Nikola Radakovic"
__email__ = "radaknikolans@gmail.com"
__credits__ = "Nikola Radakovic"
__status__ = "Development"

# --------------------------------------------------------------
# Imports
# --------------------------------------------------------------
import inspect

# ---------------------------------------------------------
# constants
# ---------------------------------------------------------


# ---------------------------------------------------------
# Useful functions
# ---------------------------------------------------------
def construct_header(data):
    """ Construct a header as prefix to log message by inspecting stack
    :param data: call sequence stack
    :return: Constructed header based on stack inspection
    """
    if data[2][3] == '<module>':
        call_function = 'main'
    else:
        call_function = data[2][3]
    line = str(data[2][2])
    return f'[{call_function}::{line}]'


# ---------------------------------------------------------
# logger based exceptions
# ---------------------------------------------------------
class LoggerError(BaseException):
    """
    Base logger exception
    """


class AssignmentError(LoggerError):
    """
    Forbidden assignment exception
    """


# --------------------------------------------------------------
# Global variables & classes
# --------------------------------------------------------------
class Log:
    """
    Main logger class for printing messages to standard output.
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

    ERROR = int(1)
    WARNING = int(2)
    INFO = int(4)
    DEBUG = int(8)
    DEBUG_2 = int(16)
    DEBUG_3 = int(32)
    ENTER_EXIT_POINT = int(64)
    ALL = int(127)

    LEVEL_COLOR = {
        ERROR: [RED, 'ERROR'],
        WARNING: [YELLOW, 'WARNING'],
        INFO: [GREEN, 'INFO'],
        DEBUG: [BLUE, 'DEBUG'],
        DEBUG_2: [CYAN, 'DEBUG_2'],
        DEBUG_3: [PURPLE, 'DEBUG_3']
    }

    def __init__(self, level=0, use_colors=False, offset=0):
        """
        Logger constructor
        :param level:
        :param use_colors:
        :param offset:
        """

        self.level = level
        self.use_colors = use_colors
        self._offset = offset
        self._use_header = False

    def _print_log(self, lvl_info, message=''):
        length = len(lvl_info[1])
        if self.use_header:
            header = construct_header(inspect.stack())
            offset = self._offset - len(header) - 4 - length
            padding = 1
        else:
            header = ''
            padding = 8 - length
            offset = 0
        print('{}{}{}{}{}:{}{}'.format(header,
                                       "".ljust(offset),
                                       lvl_info[0],
                                       lvl_info[1],
                                       self.RESET,
                                       "".ljust(padding),
                                       message))

    @property
    def use_header(self):
        """
        Getter for header usage
        :return: True or False
        """
        return self._use_header

    @property
    def offset(self):
        """
        Getter for offset
        :return: integer number
        """
        return self._offset

    @use_header.setter
    def use_header(self, use_header):
        """
        Setter for header usage
        :param use_header: True of False
        :return:
        """
        if not use_header:
            self._offset = 0
        self._use_header = use_header

    @offset.setter
    def offset(self, offset):
        """
        Setter for offset
        :param offset: integer offset
        :return:
        """
        if not self._use_header:
            raise AssignmentError('Header is not in use, so offset cannot be '
                                  'set!')
        self._offset = offset

    def append_log_level(self, level):
        """ Append the new log level to the current one
        :param level: Log level to be append
        """
        self.level |= level

    def remove_log_level(self, level):
        """ Remove log level from current setup
        :param level: Log level to be removed
        """
        self.level &= (~level)

    def info(self, message=''):
        """ Info log
        :param message: Text to be printed on this level
        """
        if (self.level & self.INFO) > 0:
            self._print_log(self.LEVEL_COLOR[self.INFO], message)

    def warning(self, message=''):
        """ Warning log
        :param message: Text to be printed on this level
        """
        if (self.level & self.WARNING) > 0:
            self._print_log(self.LEVEL_COLOR[self.WARNING], message)

    def error(self, message=''):
        """ Error log
        :param message: Text to be printed on this level
        """
        if (self.level & self.ERROR) > 0:
            self._print_log(self.LEVEL_COLOR[self.ERROR], message)

    def debug(self, message=''):
        """ Debug log
        :param message: Text to be printed on this level
        """
        if (self.level & self.DEBUG) > 0:
            self._print_log(self.LEVEL_COLOR[self.DEBUG], message)
