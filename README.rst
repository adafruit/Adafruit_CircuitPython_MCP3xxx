Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-mcp3xxx/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/mcp3xxx/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.org/adafruit/adafruit_CircuitPython_MCP3xxx.svg?branch=master
    :target: https://travis-ci.org/adafruit/adafruit_CircuitPython_MCP3xxx
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

Usage Example
=============


Single Ended
------------

.. code-block:: python

    import busio
    import digitalio
    import board
    from adafruit_mcp3xxx import adafruit_mcp3xxx

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create a mcp3008 object
    mcp = adafruit_mcp3xxx.MCP3008(spi,cs)

    # create an an adc (single-ended) on pin 0
    adc_single_ended = adafruit_mcp3xxx.AnalogIn(mcp, 0)
    print('\nADC')
    print('\tValue: ', adc_single_ended.value)
    print('\tVolts: ', adc_single_ended.volts)


Differential
------------

.. code-block:: python 

    import busio
    import digitalio
    import board
    from adafruit_mcp3xxx import adafruit_mcp3xxx

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create a mcp3008 object
    mcp = adafruit_mcp3xxx.MCP3008(spi,cs)

    # create an an adc (differential) on pin 0
    adc_diff = adafruit_mcp3xxx.AnalogIn_Differential(mcp, 0, 1)
    print('\nDifferential ADC')
    print('\tDiff. Value: ', adc_diff.value)
    print('\tDiff. Voltage: ', adc_diff.volts)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/adafruit_CircuitPython_MCP3xxx/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

Zip release files
-----------------

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-mcp3xxx --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
