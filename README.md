# STLogging
![](https://github.com/nradakovic/stlogging/workflows/Linter%20check%20-%20examples/badge.svg)

## Introduction
STLogging is a logging module that extends native Python logging module. The main idea 
of this module is to be used in large scale projects where different 
logging level is easy configurable by config files.
Features which STLogging has and extends native logging are:
1. Setup different log levels in modules, files, or functions.
2. Setup custom format or use default one.
3. Use config file to setup formats.


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

## Development
Current status of the STLogging is `development`. The new features and bugs can be tracked here: https://github.com/nradakovic/stlogging/issues
