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
        self._mcp = mcp
        self._positive_pin = positive_pin
        self._negative_pin = negative_pin
        if negative_pin is not None:
            # set up the adc for differential reads
            self._channels = []
            if self._mcp.MCP3008_DIFF_PINS:
                self._pins = self._mcp.MCP3008_DIFF_PINS
            elif self._mcp.MCP3004_DIFF_PINS:
                self._pins = self._mcp.MCP3004_DIFF_PINS
            else:
                raise TypeError('Diff. reads require MCP pins')
            self._diff_pin = self._pins.get((self._positive_pin, self._negative_pin),
                                            "Difference pin not found.")

    @property
    def value(self):
        """Returns the value of an ADC pin as an integer."""
        if self._negative_pin is not None:
            return self._mcp.read(self._diff_pin, is_differential=True)
        return self._mcp.read(self._positive_pin)

    @property
    def voltage(self):
        """Returns the voltage from the ADC pin as a floating point value."""
        if self._negative_pin is not None:
            v_in = v_in = self._mcp.read(self._diff_pin, is_differential=True)
        else:
            v_in = self._mcp.read(self._positive_pin)
        return (v_in * self._mcp.ref_voltage) / 1023
