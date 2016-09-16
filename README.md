[![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)](http://www.synapse-wireless.com/)

# Advanced SNAPpy Includes for the ATmega128RFA1

`snappyatmega` is a SNAPpy library that extends the functionality of Synapse SNAP modules that utilize the ATmega128RFA1.

## Installation

### For use in Portal

Download and extract the latest release zip file to Portal's `snappyImages` directory.
By default, this is located at `...\Documents\Portal\snappyImages` on Windows.

### For use with SNAPbuild

The easiest way to install `snappyatmega` for use with SNAPbuild is using [pip](https://pip.pypa.io/en/latest/installing.html):

    pip install git+https://github.com/synapse-wireless/snappy-atmega.git@master

Alternatively you can download the source, extract it, and install it:

    python setup.py install

## Usage

To use the `snappyatmega` library functions either import the entire library:

```python
from snappyatmega import *
```

or import just the parts you need:

```python
from snappyatmega.math import *
from snappyatmega.rtc import *
from snappyatmega.timers import *
from snappyatmega.sensors import *
```

## License

Copyright © 2016 [Synapse Wireless](http://www.synapse-wireless.com/), licensed under the [Apache License v2.0](LICENSE.md).
