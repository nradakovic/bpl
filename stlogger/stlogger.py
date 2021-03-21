#!/usr/bin/env python3
# --------------------------------------------------------------
# Copyright (C) 2021 Nikola Radakovic
# email: radaknikolans@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" STLogger module is used to write formatted messages to standard output.
"""

# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------
import sys
import json
import argparse
import logging as log

# ---------------------------------------------------------------------
# Authorship information
# ---------------------------------------------------------------------
__author__     = 'Nikola Radakovic'
__copyright__  = 'Copyright 2021, The Logger Project'
__license__    = 'MIT'
__version__    = '0.0.1'
__maintainer__ = 'Nikola Radakovic'
__email__      = 'radaknikolans@gmail.com'
__status__     = 'Development'


# ---------------------------------------------------------------------
# Global level variables wrapped from logging module
# ---------------------------------------------------------------------
NOTSET = log.NOTSET
DEBUG = log.DEBUG
INFO = log.INFO
WARNING = log.WARNING
ERROR = log.ERROR
CRITICAL = log.CRITICAL


# ---------------------------------------------------------------------
# Logger class
# ---------------------------------------------------------------------
class STLogger(log.Logger):
    """
    Implementation of logger class which is used to print logs from
    different modules, files, and functions with colored output or
    without it (several formats supported).
    """
    _MODULES = []
    _DEFAULT_NAME = 'STLogger'
    _FORMAT = (
        '%(asctime)s - '
        '%(name)s - '
        '%(levelname)s: '
        '%(message)s'
    )
    _CONFIG = None

    def __init__(self, default_name=_DEFAULT_NAME, config=None):
        """
        Constructor of the logger which will set default name for
        all modules.
        :param default_name: string name that will be used for all
                             logs which don't set name explicitly.
        :param config: string path to the json configuration.
        """
        super().__init__(name=default_name)
        if config is not None:
            with open(config) as handle:
                for raw in json.load(handle)['modules']:
                    STLogger.create_logger(raw['module'],
                                           log.getLevelName(raw['level']))

    @staticmethod
    def create_logger(module=None, level=INFO, c_format=None):
        """
        Static class which creates custom logger.
        :param module: string name of the module
        :param level: int level of supported messages (it will override
                      current level saved on module)
        :param c_format: tuple object representing format for messages
        :return: Logger objects which can be used to print messages
        """
        name = STLogger._DEFAULT_NAME
        if module is not None:
            if module not in STLogger._MODULES:
                STLogger._MODULES.append({'module': module,
                                          'level': level})
            name = module

        logger = log.getLogger(name)
        if not logger.handlers:
            stream = log.StreamHandler()
            formatter = log.Formatter(c_format if c_format is not None
                                      else STLogger._FORMAT)
            stream.setFormatter(formatter)
            logger.addHandler(stream)
            logger.setLevel(level)

        if logger.level != level:
            logger.setLevel(level)

        return logger

    @staticmethod
    def get_logger(module):
        """
        Wrapper method around logging.getLogger() to make sure the formatting
        for requested logger has been set using json config file.
        :param module: string name of the module
        :return: Logger objects which can be used to print messages
        """
        if len(STLogger._MODULES) == 0:
            raise ValueError('There are no modules set!')

        if not any(m['module'] == module for m in STLogger._MODULES):
            raise ValueError(f'Module {module} is not set')

        return log.getLogger(module)

# ---------------------------------------------------------------------
# Version and authorship info functions
# ---------------------------------------------------------------------
def authorship():
    """
    Function for printing Authorship information to the STDOUT without
    any formatting.
    """
    print(f'Author:     {__author__}')
    print(f'Copyright:  {__copyright__}')
    print(f'License:    {__license__}')
    print(f'Version:    {__version__}')
    print(f'Maintainer: {__maintainer__}')
    print(f'E-Mail:     {__email__}')
    print(f'Status:     {__status__}')


def parse_argv(argv):
    """
    Parse command line arguments
    :return: parsing object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--authorship_information',
                        dest='auth_info', action='store_false',
                        default=True)
    parser.add_argument('-v', '--version', dest='version',
                        action='store_true', default=False)
    return parser.parse_args(argv)


def main(argv=None):
    """
    Main execution function
    :return: 0 in case of success, otherwise error code
    """
    args = parse_argv(argv if argv is not None else sys.argv[1:])

    if args.auth_info:
        authorship()

    if args.version:
        print(f'{__version__}')

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
