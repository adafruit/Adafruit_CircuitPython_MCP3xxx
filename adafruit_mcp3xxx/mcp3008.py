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
`mcp3008.py`
=============================================
MCP3008 8-channel, 10-bit, analog-to-digital
converter instance.

* Author(s): Brent Rubell
"""

from .mcp3xxx import MCP3xxx

# MCP3008 Pin Mapping
P0 = 0
P1 = 1
P2 = 2
P3 = 3
P4 = 4
P5 = 5
P6 = 6
P7 = 7

class MCP3008(MCP3xxx):

    """
    MCP3008 Differential channel mapping.
        - 0: CH0 = IN+, CH1 = IN-
        - 1: CH1 = IN+, CH0 = IN-
        - 2: CH2 = IN+, CH3 = IN-
        - 3: CH3 = IN+, CH2 = IN-
        - 4: CH4 = IN+, CH5 = IN-
        - 5: CH5 = IN+, CH4 = IN-
        - 6: CH6 = IN+, CH7 = IN-
        - 7: CH7 = IN+, CH6 = IN-
    """
    MCP3008_DIFF_PINS = {
        (0, 1) : P0,
        (1, 0) : P1,
        (2, 3) : P2,
        (3, 2) : P3,
        (4, 5) : P4,
        (5, 4) : P5,
        (6, 7) : P6,
        (7, 6) : P7
    }
