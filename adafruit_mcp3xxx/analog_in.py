# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
:py:class:`~adafruit_mcp3xxx.analog_in.AnalogIn`
======================================================
AnalogIn for single-ended and
differential ADC readings.

* Author(s): Brent Rubell

.. warning::
    The ADC chips supported by this library do not use negative numbers. If the resulting
    differential read is less than 0, then the returned integer value (and voltage value) is ``0``.
    If for some reason the voltage on a channel is greater than the reference voltage or
    less than 0, then the returned integer value is ``65535`` or ``0`` respectively.

"""

from .mcp3xxx import MCP3xxx

try:
    from typing import Optional
except ImportError:
    pass


class AnalogIn:
    """AnalogIn Mock Implementation for ADC Reads.

    :param MCP3002,MCP3004,MCP3008 mcp: The mcp object.
    :param int positive_pin: Required pin for single-ended.
    :param int negative_pin: Optional pin for differential reads.
    """

    def __init__(self, mcp: MCP3xxx, positive_pin: int, negative_pin: Optional[int] = None) -> None:
        if not isinstance(mcp, MCP3xxx):
            raise ValueError("mcp object is not a sibling of MCP3xxx class.")
        self._mcp = mcp
        self._pin_setting = positive_pin
        self.is_differential = negative_pin is not None
        if self.is_differential:
            self._pin_setting = self._mcp.DIFF_PINS.get((positive_pin, negative_pin), None)
            if self._pin_setting is None:
                raise ValueError(
                    "Differential pin mapping not defined. Please read the "
                    "documentation for valid differential channel mappings."
                )

    @property
    def value(self) -> int:
        """Returns the value of an ADC pin as an integer in the range [0, 65535]."""
        # Initial result is only 10 bits.
        result = int(self._mcp.read(self._pin_setting, is_differential=self.is_differential))
        # Stretch to 16 bits and cover full range.
        return (result << 6) | (result >> 4)

    @property
    def voltage(self) -> float:
        """Returns the voltage from the ADC pin as a floating point value. Due to the 10-bit
        accuracy of the chip, returned values range from 0 to ``reference_voltage``."""
        return self.value * self._mcp.reference_voltage / 65535
