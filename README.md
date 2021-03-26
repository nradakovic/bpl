# BluePhoenix Logging (BPL)
![](https://github.com/nradakovic/stlogging/workflows/Linter%20check%20-%20examples/badge.svg)

## Introduction
BluePhoenix Logging (or short BPL) is a logging module that extends 
native Python logging module. The main idea of this module is to be used in 
large scale projects where different logging level is easy configurable by 
config files.
Features which BPL has and extends native logging are:
1. Setup different log levels in modules, files, or functions.
2. Setup custom format or use default one.
3. Use config file to setup formats.

## Usage
By importing the module `bpl` and call create_logger to init Logger 
class from native logging below:
```python
from bpl import create_logger, DEBUG

log = create_logger("AppInit", DEBUG)
log.debug("Test")
```

## License
BPL has MIT License.
For more details please visit: https://opensource.org/licenses/MIT

## Development
Current status of the BPL is `development`. The new features and bugs 
can be tracked here: https://github.com/nradakovic/bpl/issues
