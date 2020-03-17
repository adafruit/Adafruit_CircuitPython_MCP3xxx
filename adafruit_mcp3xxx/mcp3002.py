# The MIT License (MIT)
#
# Copyright (c) 2018 Brent Rubell for Adafruit
# Copyright (c) 2019 Brendan Doherty
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
:py:class:`~adafruit_mcp3xxx.MCP3002.MCP3002`
================================================
MCP3002 2-channel, 10-bit, analog-to-digital
converter instance.

* Author(s): Brent Rubell, Brendan Doherty

For proper wiring, please refer to `Package Type diagram
<http://ww1.microchip.com/downloads/en/devicedoc/21294e.pdf#G1.1011678>`_ and `Pin Description
<http://ww1.microchip.com/downloads/en/devicedoc/21294e.pdf#G1.1034774>`_ section of the MCP3002
datasheet.
"""
from .mcp3xxx import MCP3xxx

# MCP3002 Pin Mapping
P0 = 0
P1 = 1


class MCP3002(MCP3xxx):
    """
    MCP3002 Differential channel mapping. The following list of available differential readings
    takes the form ``(positive_pin, negative_pin) = (channel A) - (channel B)``.

    - (P0, P1) = CH0 - CH1
    - (P1, P0) = CH1 - CH0

    See also the warning in the `AnalogIn`_ class API.
    """

    DIFF_PINS = {(0, 1): P0, (1, 0): P1}

    def read(self, pin, is_differential=False):
        self._out_buf[0] = 0x40 | ((not is_differential) << 5) | (pin << 4)
        with self._spi_device as spi:
            # pylint: disable=no-member
            spi.write_readinto(self._out_buf, self._in_buf, out_end=2, in_end=2)
        return ((self._in_buf[0] & 0x03) << 8) | self._in_buf[1]
