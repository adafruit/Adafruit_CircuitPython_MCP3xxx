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
"""

from micropython import const
from .mcp3xxx import MCP3xxx


# MCP3002 data transfer commands
_MCP3002_OUT_BUFF = const(0x00)
_MCP3002_DIFF_READ = const(0x00)
_MCP3002_SINGLE_READ = const(0x02)

# MCP3002 Pin Mapping
P0 = 0
P1 = 1

class MCP3002(MCP3xxx):
    """
    MCP3002 Differential channel mapping.
        Use the following predefined options as the third parameter to
        :class:`~adafruit_mcp3xxx.analog_in.AnalogIn`'s contructor to obtain the differential
        value of the option's corresponding pair of channels. See `examples/` for usage.

        - ``P0`` = Channel 0 - Channel 1
        - ``P1`` = Channel 1 - Channel 0
    """
    DIFF_PINS = {
        (0, 1) : P0,
        (1, 0) : P1
    }

    def read(self, pin, is_differential=False):
        command = (_MCP3002_DIFF_READ if is_differential else _MCP3002_SINGLE_READ) << 6
        command |= pin << 2
        self._out_buf[0] = command
        self._out_buf[1] = _MCP3002_OUT_BUFF
        self._out_buf[2] = _MCP3002_OUT_BUFF
        with self._spi_device as spi:
            #pylint: disable=no-member
            spi.write_readinto(self._out_buf, self._in_buf, out_start=0,
                               out_end=len(self._out_buf), in_start=0, in_end=len(self._in_buf))
        result = (self._in_buf[0] & 0x01) << 9
        result |= self._in_buf[1] << 1
        result |= self._in_buf[2] >> 7
        return result
