# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
:py:class:`~adafruit_mcp3xxx.mcp3208.MCP3208`
=============================================================
MCP3208 8-channel, 12-bit, analog-to-digital
converter instance.

* Author(s): Brent Rubell, Kevin J. Walters

For proper wiring, please refer to `Package Types diagram
<https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/21298e.pdf>`_
and `Pin Description section
<https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/21298e.pdf#G1.1041174>`_
of the MCP3204/MCP3208 datasheet.
"""

from .mcp3xxx import MCP3xxx

# MCP3208 Pin Mapping
P0 = 0
P1 = 1
P2 = 2
P3 = 3
P4 = 4
P5 = 5
P6 = 6
P7 = 7


class MCP3208(MCP3xxx):
    """
    MCP3208 Differential channel mapping. The following list of available differential readings
    takes the form ``(positive_pin, negative_pin) = (channel A) - (channel B)``.

    - (P0, P1) = CH0 - CH1
    - (P1, P0) = CH1 - CH0
    - (P2, P3) = CH2 - CH3
    - (P3, P2) = CH3 - CH2
    - (P4, P5) = CH4 - CH5
    - (P5, P4) = CH5 - CH4
    - (P6, P7) = CH6 - CH7
    - (P7, P6) = CH7 - CH6

    See also the warning in the `AnalogIn`_ class API.
    """

    BITS = 12
    DIFF_PINS = {
        (0, 1): P0,
        (1, 0): P1,
        (2, 3): P2,
        (3, 2): P3,
        (4, 5): P4,
        (5, 4): P5,
        (6, 7): P6,
        (7, 6): P7,
    }

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
        self._out_buf[0] = 0x04 | ((not is_differential) << 1) | (pin >> 2)
        self._out_buf[1] = (pin & 0x03) << 6
        with self._spi_device as spi:
            # pylint: disable=no-member
            spi.write_readinto(self._out_buf, self._in_buf)
        return ((self._in_buf[1] & 0x0F) << 8) | self._in_buf[2]
