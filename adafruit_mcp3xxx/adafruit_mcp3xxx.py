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

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx.git"

# imports
from micropython import const
import digitalio
from adafruit_bus_device.spi_device import SPIDevice

# configuration values
MCP3008_OUT_BUFF      = const(0x00)
MCP3008_DIFF_READ     = const(0b10)
MCP3008_SINGLE_READ   = const(0b11)


class MCP3xxx(object):
  def __init__(self, spi_bus, cs, max_voltage=3.3):
    """
    Base MCP3xxx Interface

    :param ~busdevice.SPIDevice spi_bus: SPI bus the ADC is on.
    :param ~digitalio.DigitalInOut cs: Chip Select pin.
    :param int max_voltage: Maximum voltage into the ADC, defaults to 3.3v.
    :param bool differential: If true, ADC operates in differential mode.
    """
    self.spi_device = SPIDevice(spi_bus, cs)
    self.out_buf = bytearray(3)
    self.in_buf = bytearray(3)
    self.max_voltage = max_voltage

  def _read_pin(self, pin):
      """Subclasses should override this function to return a value for the
      requested pin as a signed integer value.
      """
      raise NotImplementedError('Subclass must implement _read_pin function!')

  def _read_pin_volts(self, pin):
      """Subclasses should override this function to return a value for the
      requested pin as a float value.
      """
      raise NotImplementedError('Subclass must implement _read_pin_volts function!')

  def _read(self, pin, is_differential=False):
    """SPI transfer for ADC reads.

    params:
      int pin: individual pin or differential.
      bool is_differential: single-ended or differential read.
    """
    # build adc read command
    if is_differential:
      command = MCP3008_DIFF_READ << 6
    else:
      command = MCP3008_SINGLE_READ << 6
    command |= ((pin & 0x07) << 3)
    self.out_buf[0] = command
    self.out_buf[1] = MCP3008_OUT_BUFF
    self.out_buf[2] = MCP3008_OUT_BUFF
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


class MCP3008(MCP3xxx):
    """MCP3008 10-bit single ended analog to digital converter instance
    
    mcp = MCP3008(spi_bus, cs)
    """
    def __init__(self, spi_bus, cs):
        super(MCP3008, self).__init__(self,spi_bus, cs)
        self.pin_count = 7 # mcp3008 has 8ch.

    def _read_pin(self, pin):
        assert 0 <= pin <= self.pin_count, 'Pin must be a value between 0-7'
        return self._read(pin)

    def _read_pin_volts(self, pin, voltage):
      assert 0 <= pin <= 7, 'Pin must be a value between 0-7'
      raw_read = self._read(pin)
      return (raw_read * voltage) / 1023


class AnalogIn(object):
  """AnalogIn for ADC readings.
  
  adc0 = mcp3xxx.AnalogIn(mcp, 0)

  :param adc: mcp3xxx object
  :param pin: mcp3xx analog pin
  """
  def __init__(self, adc, pin):
    self._adc = adc
    self._pin = pin

  @property
  def value(self):
    """ADC pin raw reading."""
    return self._adc._read_pin(self._pin)
  
  @property
  def volts(self):
    """ADC pin reading in volts."""
    return self._adc._read_pin_volts(self._pin, self._adc.max_voltage)