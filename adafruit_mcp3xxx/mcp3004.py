# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
:py:class:`~adafruit_mcp3xxx.mcp3004.MCP3004`
================================================
MCP3004 4-channel, 10-bit, analog-to-digital
converter instance.

* Author(s): Brent Rubell, Kevin J. Walters

For proper wiring, please refer to `Package Types diagram
<https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf#page=1>`_ and `Pin Description section
<https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf#G1.1035093>`_ of the MCP3004/MCP3008
datasheet.
"""

from .mcp3xxx import MCP3xxx

try:
    import typing

    from busio import SPI
    from digitalio import DigitalInOut
except ImportError:
    pass

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

    BITS = 10
    DIFF_PINS = {(0, 1): P0, (1, 0): P1, (2, 3): P2, (3, 2): P3}

    def read(self, pin: int, is_differential: bool = False) -> int:
        """SPI Interface for MCP3xxx-based ADCs reads. Due to 10-bit accuracy, the returned
        value ranges [0, 1023].

        :param int pin: individual or differential pin.
        :param bool is_differential: single-ended or differential read.

        .. note:: This library offers a helper class called `AnalogIn`_ for both single-ended
            and differential reads. If you opt to not implement `AnalogIn`_ during differential
            reads, then the ``pin`` parameter should be the first of the two pins associated with
            the desired differential channel mapping.
        """
        self._out_buf[1] = ((not is_differential) << 7) | (pin << 4)
        with self._spi_device as spi:
            # pylint: disable=no-member
            spi.write_readinto(self._out_buf, self._in_buf)
        return ((self._in_buf[1] & 0x03) << 8) | self._in_buf[2]
