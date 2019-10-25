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
:py:class:`~adafruit_mcp3xxx.analog_in.AnalogIn`
======================================================
AnalogIn for single-ended and
differential ADC readings.

* Author(s): Brent Rubell

.. note:: The ADC chips' input pins (AKA "channels") are aliased in this library as integer
    variables whose names start with "P". Each module that contains a driver class for a
    particular ADC chip (in this library) has these aliases predefined accordingly. This is done
    for code readability and prevention of erroneous SPI commands. The following example code
    explains this best:

    .. code-block:: python

        >>> import adafruit_mcp3xxx.mcp3008 as MCP
        >>> print('channel', MCP.P0)
        channel 0
        >>> print('channel', MCP.P7)
        channel 7
        >>> print('channel', MCP.P8)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        AttributeError: 'module' object has no attribute 'P8'
"""

from .mcp3xxx import MCP3xxx

class AnalogIn():
    """AnalogIn Mock Implementation for ADC Reads.

    :param ~mcp3002.MCP3002,~mcp3004.MCP3004,~mcp3008.MCP3008 mcp: The mcp object.
    :param int positive_pin: Required pin for single-ended.
    :param int negative_pin: Optional pin for differential reads.

    .. important::
        The ADC chips supported by this library do not handle negative numbers when returning the
        differential read of 2 channels. If the resulting differential read is less than 0, the
        returned integer is ``0``. If for some reason the voltage on a channel is greater than the
        reference voltage (Vin) or less than 0, then the returned integer is ``65472‬`` or ``0``
        (applies to single ended and differential reads).

        It is also worth noting that the differential reads (comparisons done by the ADC chip) are
        limited to certain pairs of channels. Please refer to the driver class of your ADC chip for
        a list of available differential mappings (comparisons). Otherwise, it is recommended to
        compute the differences between single-ended reads of separate channels for more flexible
        results.
    """
    def __init__(self, mcp, positive_pin, negative_pin=None):
        if not isinstance(mcp, MCP3xxx):
            raise ValueError("mcp object is not a sibling of MCP3xxx class.")
        self._mcp = mcp
        self._pin_setting = positive_pin
        self.is_differential = negative_pin is not None
        if self.is_differential:
            self._pin_setting = self._mcp.DIFF_PINS.get((self._pin_setting, negative_pin), None)
        if self._pin_setting is None:
            # this scope (kinda) checks positive_pin datatype also
            raise ValueError("Differential pin mapping not defined. Please read the docs.")

    @property
    def value(self):
        """Returns the value of an ADC pin as an integer."""
        return self._mcp.read(self._pin_setting, is_differential=self.is_differential) << 6

    @property
    def voltage(self):
        """Returns the voltage from the ADC pin as a floating point value."""
        return (self.value * self._mcp.reference_voltage) / 65535
