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


  def _read(self, channel, is_differential=False):
    """ SPI transfer for ADC reads.

    params:
      int channel: individual channel or differential.
      bool is_differential: single-ended or differential read.
    """
    # build adc read command
    if is_differential:
      command = 0b10 << 6
    else:
      command = 0b11 << 6
    command |= ((channel & 0x07) << 3)
    self.out_buf[0] = command
    self.out_buf[1] = 0x00
    self.out_buf[2] = 0x00
    # spi transfer
    with self.spi_device as spi:
      spi.write_readinto(self.out_buf, self.in_buf, out_start=0, 
        out_end=len(self.out_buf), in_start=0, in_end=len(self.in_buf))
    # parse and ret. result (10b) 
    result = (self.in_buf[0] & 0x01) << 9
    result |= (self.in_buf[1] & 0xFF) << 1
    result |= (self.in_buf[2] & 0x80) >> 7
    result &= 0x3FF
    return result 


  def read_adc(self, channel):
    """Read a single ADC channel and return the ADC value
    as an integer. Channel must be a value within 0-7.
    """
    assert 0 <= channel <= 7, 'Channel number must be a value within 0-7!'
    return self._read(channel)


  def read_volts(self, channel, voltage=3.3):
    """Read a single ADC channel and return the ADC value
    as a float. Channel must be a value within 0-7.
    """
    assert 0 <= channel <= 7, 'Channel must be a value within 0-7!'
    raw_read = self.read_adc(channel)
    return (raw_read * voltage) / 1023

  def read_adc_difference(self, differential):
    """Read the difference between two ADC channels and return the
    value as an integer. Differential must be one of:
    - 0: Return channel 0 minus channel 1
    - 1: Return channel 1 minus channel 0
    - 2: Return channel 2 minus channel 3
    - 3: Return channel 3 minus channel 2
    - 4: Return channel 4 minus channel 5
    - 5: Return channel 5 minus channel 4
    - 6: Return channel 6 minus channel 7
    - 7: Return channel 7 minus channel 6
    """
    assert 0 <= differential <= 7, 'Differential must be a value within 0-7!'
    return self._read(differential, is_differential=True)
  
  def read_volts_difference(self, differential, voltage=3.3):
    """Read the difference between two ADC channels and return the
    voltage as an float. Differential must be one of:
    - 0: Return channel 0 minus channel 1
    - 1: Return channel 1 minus channel 0
    - 2: Return channel 2 minus channel 3
    - 3: Return channel 3 minus channel 2
    - 4: Return channel 4 minus channel 5
    - 5: Return channel 5 minus channel 4
    - 6: Return channel 6 minus channel 7
    - 7: Return channel 7 minus channel 6
    """
    assert 0 <= differential <= 7, 'Differential must be a value within 0-7!'
    raw_read = self.read_adc_difference(differential)
    return (raw_read * voltage) / 1023