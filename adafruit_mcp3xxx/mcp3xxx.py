# The MIT License (MIT)
#
# Copyright (c) 2018 ladyada for Adafruit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
:py:class:`~adafruit_mcp3xxx.adafruit_mcp3xxx.MCP3xxx`
============================================================

CircuitPython Library for MCP3xxx ADCs with SPI

* Author(s): ladyada, Brent Rubell

Implementation Notes
--------------------

**Hardware:**

* Adafruit `MCP3008 8-Channel 10-Bit ADC with SPI
  <https://www.adafruit.com/product/856>`_ (Product ID: 856)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

.. note:: The ADC chips' input pins (AKA "channels") are aliased in this library
    as integer variables whose names start with "P" (eg ``MCP3008.P0`` is channel 0 on the MCP3008
    chip). Each module that contains a driver class for a particular ADC chip has these aliases
    predefined accordingly. This is done for code readability and prevention of erroneous SPI
    commands.

.. important::
    The differential reads (comparisons done by the ADC chip) are limited to certain pairs of
    channels. These predefined pairs are referenced in this documentation as differential
    channel mappings. Please refer to the driver class of your ADC chip (`MCP3008`_,
    `MCP3004`_, `MCP3002`_) for a list of available differential channel mappings.
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx.git"

from adafruit_bus_device.spi_device import SPIDevice


class MCP3xxx:
    """
    This abstract base class is meant to be inherited by `MCP3008`_, `MCP3004`_,
    or `MCP3002`_ child classes.

    :param ~adafruit_bus_device.spi_device.SPIDevice spi_bus: SPI bus the ADC is connected to.
    :param ~digitalio.DigitalInOut cs: Chip Select Pin.
    :param float ref_voltage: Voltage into (Vin) the ADC.
    """

    def __init__(self, spi_bus, cs, ref_voltage=3.3):
        self._spi_device = SPIDevice(spi_bus, cs)
        self._out_buf = bytearray(3)
        self._in_buf = bytearray(3)
        self._ref_voltage = ref_voltage

    @property
    def reference_voltage(self):
        """Returns the MCP3xxx's reference voltage. (read-only)"""
        return self._ref_voltage

    def read(self, pin, is_differential=False):
        """SPI Interface for MCP3xxx-based ADCs reads. Due to 10-bit accuracy, the returned
        value ranges [0, 1023].

        :param int pin: individual or differential pin.
        :param bool is_differential: single-ended or differential read.

        .. note:: This library offers a helper class called `AnalogIn`_ for both single-ended
            and differential reads. If you opt to not implement `AnalogIn`_ during differential
            reads, then the ``pin`` parameter should be the first of the two pins associated with
            the desired differential channel mapping.
        """
        self._out_buf[1] = ((not is_differential) << 7) | (pin << 4)
        with self._spi_device as spi:
            # pylint: disable=no-member
            spi.write_readinto(self._out_buf, self._in_buf)
        return ((self._in_buf[1] & 0x03) << 8) | self._in_buf[2]
