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
`adafruit_mcp3xxx.py`
================================================

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
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx.git"


from micropython import const
from adafruit_bus_device.spi_device import SPIDevice

# MCP3004/008 data transfer commands
_MCP30084_OUT_BUFF = const(0x00)
_MCP30084_DIFF_READ = const(0x02)
_MCP30084_SINGLE_READ = const(0x3)


class MCP3xxx:
    """
    MCP3xxx Interface.

    params:
        :param ~busdevice.SPIDevice spi_bus: SPI bus the ADC is connected to.
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
        """Returns the MCP3xxx's reference voltage."""
        return self._ref_voltage

    def read(self, pin, is_differential=False):
        """SPI Interface for MCP3xxx-based ADCs reads.

        params:
            :param pin: individual or differential pin.
            :param bool is_differential: single-ended or differential read.
        """
        command = (_MCP30084_DIFF_READ if is_differential else _MCP30084_SINGLE_READ) << 6
        command |= pin << 3
        self._out_buf[0] = command
        self._out_buf[1] = _MCP30084_OUT_BUFF
        self._out_buf[2] = _MCP30084_OUT_BUFF
        with self._spi_device as spi:
            #pylint: disable=no-member
            spi.write_readinto(self._out_buf, self._in_buf, out_start=0,
                               out_end=len(self._out_buf), in_start=0, in_end=len(self._in_buf))
        result = (self._in_buf[0] & 0x01) << 9
        result |= self._in_buf[1] << 1
        result |= self._in_buf[2] >> 7
        return result
