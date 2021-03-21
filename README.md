# STLogger
![](https://github.com/nradakovic/logger/workflows/static_code_validation_src/badge.svg)
![](https://github.com/nradakovic/logger/workflows/static_code_validation_tests/badge.svg)

## Introduction
STLogging is a logger module that extends native logging module. The main idea 
of this module is to be used in large scale projects here different 
logging level is easy configurable by config files. 
Features which STLogger introduce compared to native logger are:
1. Option to colorize level name in the message for different platform 
without using any third party module. (not 
supported yet)
2. Option to setup custom format or to choose one of already predefined.
3. Option to setup different log levels in modules, files, or functions.

## Usage
By importing the module `stlogger` the main logger class can be used as shown
 below:
```python
from stlogging import create_logger, DEBUG

log = create_logger("AppInit", DEBUG)
log.debug("Test")
```

## License
STLogger has MIT License.
For more details please visit: https://opensource.org/licenses/MIT
