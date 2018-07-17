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
`adafruit_MCP3xxx`
================================================

CircuitPython Library for MCP3xxx ADCs with SPI

* Author(s): ladyada

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
  
.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
from adafruit_bus_device.spi_device import SPIDevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx.git"

class MCP3008:
  """
  Driver for the MCP3008 8-channel, 10bit ADC
  """
  def __init__(self, spi, cs):
    self.spi_device = SPIDevice(spi, cs)
    self.out_buf = bytearray(3)
    self.in_buf = bytearray(3)

  def _read_channel(self, channel=0):
    assert 0 <= channel <= 7, 'Channel must be a value within 0-7!'
    command = (0x01 << 7)
    command |= (1 << 6)
    command |= ((channel & 0x07) << 3)
    self.out_buf[0] = command
    self.out_buf[1] = 0x00
    self.out_buf[2] = 0x00
    with self.spi_device as spi:
      spi.write_readinto(self.out_buf, self.in_buf, out_start=0, out_end=len(self.out_buf), in_start=0, in_end=len(self.in_buf))
    result = (self.in_buf[0] & 0x01) << 9
    result |= (self.in_buf[1] & 0xFF) << 1
    result |= (self.in_buf[2] & 0x80) >> 7
    result &= 0x3FF
    return result 

  def adc_volts(self, channel, voltage=3.3):
    """single-ended adc voltage read."""
    adc_value = self._read_channel(channel)
    return (adc_value * voltage) / 1023


  def adc_value(self, channel):
    """single-ended raw ADC Value (0-1023)."""
    return self._read_channel(channel)
