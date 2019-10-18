# The MIT License (MIT)
#
# Copyright (c) 2018 Brent Rubell for Adafruit
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
:py:class:`~adafruit_mcp3xxx.analog_in.AnalogIn`
======================================================
AnalogIn for single-ended and
differential ADC readings.

* Author(s): Brent Rubell
"""

from .mcp3xxx import MCP3xxx

class AnalogIn():
    """AnalogIn Mock Implementation for ADC Reads.

    :param ~mcp3002.MCP3002,~mcp3004.MCP3004,~mcp3008.MCP3008 mcp: The mcp object.
    :param int positive_pin: Required pin for single-ended.
    :param int negative_pin: Optional pin for differential reads.
    """
    def __init__(self, mcp, positive_pin, negative_pin=None):
        if not issubclass(mcp, MCP3xxx):
            raise ValueError("mcp object is not a sibling of MCP3xxx class.")
        self._mcp = mcp
        self._pin_setting = positive_pin
        self.is_differential = negative_pin is not None
        if self.is_differential:
            self._pin_setting = self._mcp.DIFF_PINS.get((self._pin_setting, negative_pin), None)
        if self._pin_setting is None:
            raise ValueError("Differential pin mapping not defined. Please read the docs.")

    @property
    def value(self):
        """Returns the value of an ADC pin as an integer."""
        return self._mcp.read(self._pin_setting, is_differential=self.is_differential) << 6

    @property
    def voltage(self):
        """Returns the voltage from the ADC pin as a floating point value."""
        return (self.value * self._mcp.reference_voltage) / 65535
