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

""" STLogging module is used to write formatted messages to standard output.
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
# Private configuration variables
# ---------------------------------------------------------------------
_MODULES = []
_DEFAULT_NAME = 'stlogging'
_FORMAT = (
    '%(asctime)s - '
    '%(name)s - '
    '%(levelname)s: '
    '%(message)s'
)
_CONFIG = None

# ---------------------------------------------------------------------
# Public level variables wrapped from logging module
# ---------------------------------------------------------------------
NOTSET = log.NOTSET
DEBUG = log.DEBUG
INFO = log.INFO
WARNING = log.WARNING
ERROR = log.ERROR
CRITICAL = log.CRITICAL


# ---------------------------------------------------------------------
# Public logging functions
# ---------------------------------------------------------------------
def set_loggers(config):
    """
    Function to set loggers from JSON configuration file
    :param config: string path to the json configuration.
    """
    with open(config) as handle:
        for raw in json.load(handle)['modules']:
            create_logger(raw['module'],
                          log.getLevelName(raw['level']))


def create_logger(module=None, level=INFO, c_format=None, stream=None):
    """
    Function for setting logger assigned to specific module with custom format
    and stream.
    :param module: string name of the module
    :param level: int level of supported messages (it will override
                  current level saved on module)
    :param c_format: tuple object representing format for messages, default
                     stdout
    :param stream: stream object for redirecting print output, default None
    :return: Logger objects which can be used to print messages
    """
    name = _DEFAULT_NAME
    if module is not None:
        name = module

    if not any(m['module'] == module for m in _MODULES):
        _MODULES.append({'module': module, 'level': level})

    logger = log.getLogger(name)
    if not logger.handlers:
        stream_handler = log.StreamHandler(stream)
        formatter = log.Formatter(c_format if c_format is not None
                                  else _FORMAT)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.setLevel(level)

    if logger.level != level:
        logger.setLevel(level)

    return logger


def get_logger(module):
    """
    Wrapper function around logging.getLogger() to make sure the formatting
    for requested logger has been set using json config file.
    :param module: string name of the module
    :return: Logger objects which can be used to print messages
    """
    if len(_MODULES) == 0:
        raise ValueError('There are no modules set!')

    if not any(m['module'] == module for m in _MODULES):
        raise ValueError(f'Module {module} is not set')

    return log.getLogger(module)

def remove_stream_handler(module, stream):
    """
    Method for removing stream handler from logger
    :return: ---
    """
    if len(_MODULES) == 0:
        raise ValueError('There are no modules set!')

    if not any(m['module'] == module for m in _MODULES):
        raise ValueError(f'Module {module} is not set')

    logger = log.getLogger(module)
    logger.removeHandler(log.StreamHandler(stream))

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
