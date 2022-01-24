Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-mcp3xxx/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/mcp3xxx/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/actions/
    :alt: Build Status

CircuitPython library for the MCP3xxx series of analog-to-digital converters.

Currently supports:

*  `MCP3008: 8-Channel 10-Bit ADC With SPI Interface <https://www.adafruit.com/product/856>`_


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-mcp3xxx/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-mcp3xxx

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-mcp3xxx

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-mcp3xxx

Usage Example
=============


MCP3008 Single Ended
---------------------

.. code-block:: python

    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)

    print('Raw ADC Value: ', chan.value)
    print('ADC Voltage: ' + str(chan.voltage) + 'V')


MCP3008 Differential
--------------------

.. code-block:: python

    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create a differential ADC channel between Pin 0 and Pin 1
    chan = AnalogIn(mcp, MCP.P0, MCP.P1)

    print('Differential ADC Value: ', chan.value)
    print('Differential ADC Voltage: ' + str(chan.voltage) + 'V')

MCP3004 Single-Ended
---------------------

.. code-block:: python

    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3004 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3004(spi, cs)

    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)

    print('Raw ADC Value: ', chan.value)
    print('ADC Voltage: ' + str(chan.voltage) + 'V')

MCP3004 Differential
--------------------

.. code-block:: python

    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3004 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3004(spi, cs)

    # create a differential ADC channel between Pin 0 and Pin 1
    chan = AnalogIn(mcp, MCP.P0, MCP.P1)

    print('Differential ADC Value: ', chan.value)
    print('Differential ADC Voltage: ' + str(chan.voltage) + 'V')



Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/mcp3xxx/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/adafruit_CircuitPython_MCP3xxx/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
