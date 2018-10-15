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
`analog_in`
==============================
AnalogIn for single-ended and
differential ADC readings.

* Author(s): Brent Rubell
"""

class AnalogIn():
    """AnalogIn Mock Implementation for ADC Reads."""

    def __getitem__(self, key):
        return self._channels[self._pins[key]]

    def __init__(self, mcp, positive_pin, negative_pin=None):
        """AnalogIn

        :param mcp: The mcp object.
        :param ~digitalio.DigitalInOut positive_pin: Required pin for single-ended.
        :param ~digitalio.DigitalInOut negative_pin: Optional pin for differential reads.
        """
        self._mcp = mcp
        self._pin_setting = positive_pin
        self._negative_pin = negative_pin
        self.is_differential = False
        if negative_pin is not None:
            self.is_differential = True
            self._channels = []
            try:
                self._pins = self._mcp.MCP3008_DIFF_PINS
            except AttributeError:
                self._pins = self._mcp.MCP3004_DIFF_PINS
            self._pin_setting = self._pins.get((self._pin_setting, self._negative_pin),
                                               "Difference pin not found.")

    @property
    def value(self):
        """Returns the value of an ADC pin as an integer."""
        return self._mcp.read(self._pin_setting, is_differential=self.is_differential) << 6

    @property
    def voltage(self):
        """Returns the voltage from the ADC pin as a floating point value."""
        return (self.value * self._mcp.reference_voltage) / 65535
