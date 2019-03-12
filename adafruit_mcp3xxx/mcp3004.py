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
`mcp3004.py`
================================================
MCP3004 4-channel, 10-bit, analog-to-digital
converter instance.

* Author(s): Brent Rubell
"""

from .mcp3xxx import MCP3xxx

# MCP3004 Pin Mapping
P0 = 0
P1 = 1
P2 = 2
P3 = 3

class MCP3004(MCP3xxx):

    """
    MCP3004 Differential channel mapping.
        - 0: CH0 = IN+, CH1 = IN-
        - 1: CH1 = IN+, CH0 = IN-
        - 2: CH2 = IN+, CH3 = IN-
        - 3: CH3 = IN+, CH2 = IN-
    """
    MCP3004_DIFF_PINS = {
        (0, 1) : P0,
        (1, 0) : P1,
        (2, 3) : P2,
        (3, 2) : P3
    }
