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
`Differential_AnalogIn.py`
================================================

Differential AnalogIn implementation for mcp3xxx ADCs.
* Author(s): Brent Rubell
"""


class Differential_AnalogIn():

    def __getitem__(self, key):
        return self._channels[self._mcp.MCP3008_DIFF_PINS[key]]

    def __init__(self, mcp, pin_1, pin_2):
        self._mcp = mcp
        self._channels = []
        self._pin_1 = _pin_1
        self._pin_2 = pin_2
        
    @property
    def value(self):
        """calls read, returns differential value"""
        diff_pin = self._mcp.MCP3008_DIFF_PINS.get((self._pin_1, self._pin_2), "Difference pin not found.")
        return self._mcp.read(self._pin, is_differential=True)

    @property
    def voltage(self):
        """calls read, performs differential voltage calculation"""
        diff_pin = self._mcp.MCP3008_DIFF_PINS.get((self._pin_1, self._pin_2), "Difference pin not found.")
        v_in = self._mcp.read(self._pin, is_differential=True)
        return (v_in * voltage) / 1023