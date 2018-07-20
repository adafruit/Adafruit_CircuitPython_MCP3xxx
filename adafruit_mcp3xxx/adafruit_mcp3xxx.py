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

# differential pin pairs -> channel
MCP3008_DIFF_PINS = { 
                  (0,1) : 0,
                  (1,0) : 1,
                  (2,3) : 2,
                  (3,2) : 3,
                  (4,5) : 4,
                  (5,4) : 5,
                  (6,7) : 6,
                  (6,6) : 7
}

class MCP3xxx(object):
  def __init__(self, spi_bus, cs, max_voltage=3.3):
    """
    Base MCP3xxx Interface

    :param ~busdevice.SPIDevice spi_bus: SPI bus the ADC is on.
    :param ~digitalio.DigitalInOut cs: Chip Select pin.
    :param int max_voltage: Maximum voltage into the ADC, defaults to 3.3v.
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
    if (pin < 0 or pin > 7):
      raise ValueError('Pin must be a value between 0 and 7')
    # build adc read command
    if is_differential == True:
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
    """MCP3008 10-bit analog to digital converter instance.
    
    mcp = adafruit_mcp3xxx.MCP3008(spi,cs)
    """
    def __init__(self, spi_bus, cs):
        super(MCP3008, self).__init__(spi_bus, cs)
        self.pin_count = 7 #mcp3008 has 8channels.

    def _read_pin(self, pin):
      """Reads a MCP3008 pin, returns the value as an integer."""
      return self._read(pin)

    def _read_pin_volts(self, pin, voltage):
      """Reads a MCP3008 pin, returns the voltage as a floating point value."""
      v_in = self._read(pin)
      return (v_in * voltage) / 1023
    
    def _read_pin_differential(self, diff_pin):
      """Reads a MCP3008 differential pin value, returns the value as an integer."""      
      return self._read(diff_pin, is_differential=True)
    
    def _read_pin_volts_differential(self, diff_pin, voltage):
      """Reads a MCP3008 differential pin value, returns the voltage as a floating point value."""
      v_in = self._read(diff_pin, is_differential=True)
      return (v_in * voltage) / 1023


class AnalogIn(object):
  """AnalogIn for single-ended ADC readings.
  
  adc = adafruit_mcp3xxx.AnalogIn(mcp, pin)

  :param adc: mcp3xxx object.
  :param pin: mcp3xxx analog pin.
  """
  def __init__(self, adc, pin):
    self._adc = adc
    self._pin = pin

  @property
  def value(self):
    """Returns the value of an ADC pin as an integer.
    """
    return self._adc._read_pin(self._pin)

  @property
  def volts(self):
    """Returns the voltage from an ADC pin as a floating point value.
    """
    return self._adc._read_pin_volts(self._pin, self._adc.max_voltage)


class AnalogIn_Differential(object):
  """Reads the difference between two signals

  adc = adafruit_mcp3xxx.AnalogIn_Differential(mcp, pin_1, pin_2)

  :param adc: mcp3xxx object.
  :param pin_1: mcp3xxx analog pin 1.
  :param pin_2: mcp3xxx analog pin 2.
  """

  def __getitem__(self, key):
    return self._channels[MCP3008_DIFF_PINS[key]]

  def __init__(self, adc, pin_1, pin_2):
    self._adc = adc
    self._pin_1 = pin_1
    self._pin_2 = pin_2

  @property
  def value(self):
    """Returns the value from a differential read across two pins as an integer.
    """
    diff_pin = MCP3008_DIFF_PINS.get((self._pin_1,self._pin_2), "Difference pin not found.")
    return self._adc._read_pin_differential(diff_pin)

  @property
  def volts(self):
    """Returns the voltage from a differential read across two pins as a floating point value.
    """
    diff_pin = MCP3008_DIFF_PINS.get((self._pin_1,self._pin_2), "Difference pin not found.")
    return self._adc._read_pin_volts_differential(diff_pin, self._adc.max_voltage)