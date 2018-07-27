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
`analog_in.py`
================================================
AnalogIn for single-ended ADC readings.

* Author(s): Brent Rubell
"""

class AnalogIn():
    """AnalogIn Mock Implementation for ADC Reads."""
    def __init__(self, mcp, pin):
        self._mcp = mcp
        self._pin = pin

    @property
    def value(self):
        """Returns the value of an ADC pin as an integer."""
        return self._mcp.read(self._pin)

    @property
    def voltage(self):
        """Returns the voltage from the ADC pin as a floating point value."""
        v_in = self._mcp.read(self._pin)
        return (v_in * self._mcp.ref_voltage) / 1023
