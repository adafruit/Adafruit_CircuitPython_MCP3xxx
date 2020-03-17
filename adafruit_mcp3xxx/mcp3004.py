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
:py:class:`~adafruit_mcp3xxx.mcp3004.MCP3004`
================================================
MCP3004 4-channel, 10-bit, analog-to-digital
converter instance.

* Author(s): Brent Rubell

For proper wiring, please refer to `Package Types diagram
<https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf#page=1>`_ and `Pin Description section
<https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf#G1.1035093>`_ of the MCP3004/MCP3008
datasheet.
"""

from .mcp3xxx import MCP3xxx

# MCP3004 Pin Mapping
P0 = 0
P1 = 1
P2 = 2
P3 = 3


class MCP3004(MCP3xxx):
    """
    MCP3004 Differential channel mapping. The following list of available differential readings
    takes the form ``(positive_pin, negative_pin) = (channel A) - (channel B)``.

    - (P0, P1) = CH0 - CH1
    - (P1, P0) = CH1 - CH0
    - (P2, P3) = CH2 - CH3
    - (P3, P2) = CH3 - CH2

    See also the warning in the `AnalogIn`_ class API.
    """

    DIFF_PINS = {(0, 1): P0, (1, 0): P1, (2, 3): P2, (3, 2): P3}

    def __init__(self, spi_bus, cs, ref_voltage=3.3):
        super(MCP3004, self).__init__(spi_bus, cs, ref_voltage=ref_voltage)
        self._out_buf[0] = 0x01
