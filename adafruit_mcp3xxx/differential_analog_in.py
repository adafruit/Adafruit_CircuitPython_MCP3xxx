# The MIT License (MIT)
#
# Copyright (c) 2018 Brent Rubell for Adafruit Industries
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
`differential_analogin.py`
======================================================
Differential ADC read for mcp3xxx ADCs.

* Author(s): Brent Rubell
"""

class DifferentialAnalogIn():

    def __getitem__(self, key):
        return self._channels[self._pins[key]]

    def __init__(self, mcp, pin_1, pin_2):
        self._mcp = mcp
        self._pin_1 = pin_1
        self._pin_2 = pin_2
        self._channels = []
        if self._mcp.MAX_PIN == 7:
            self._pins = self._mcp.MCP3008_DIFF_PINS
        elif self._mcp.MAX_PIN == 3:
            self._pins = self._mcp.MCP3004_DIFF_PINS
        else:
            raise TypeError('MCP object requires MAX_PIN')


    @property
    def value(self):
        """calls read, returns differential value"""
        diff_pin = self._pins.get((self._pin_1, self._pin_2), "Difference pin not found.")
        return self._mcp.read(diff_pin, is_differential=True)

    @property
    def voltage(self):
        """calls read, performs differential voltage calculation"""
        diff_pin = self._pins.get((self._pin_1, self._pin_2), "Difference pin not found.")
        v_in = self._mcp.read(diff_pin, is_differential=True)
        return (v_in * self._mcp.ref_voltage) / 1023
