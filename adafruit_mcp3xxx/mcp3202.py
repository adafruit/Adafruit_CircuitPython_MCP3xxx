# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Brendan Doherty Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
:py:class:`~adafruit_mcp3xxx.MCP3202.MCP3202`
================================================
MCP3202 2-channel, 12-bit, analog-to-digital
converter instance.

* Author(s): Brent Rubell, Brendan Doherty, Kevin J. Walters

For proper wiring, please refer to `Package Type diagram
<https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/21034F.pdf>`_
and `Pin Description
<https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/21034F.pdf#G1.1063009>`_
section of the MCP3202 datasheet.
"""
from .mcp3xxx import MCP3xxx

# MCP3202 Pin Mapping
P0 = 0
P1 = 1


class MCP3202(MCP3xxx):
    """
    MCP3202 Differential channel mapping. The following list of available differential readings
    takes the form ``(positive_pin, negative_pin) = (channel A) - (channel B)``.

    - (P0, P1) = CH0 - CH1
    - (P1, P0) = CH1 - CH0

    See also the warning in the `AnalogIn`_ class API.
    """

    BITS = 12
    DIFF_PINS = {(0, 1): P0, (1, 0): P1}

    def read(self, pin: int, is_differential: bool = False) -> int:
        """SPI Interface for MCP3xxx-based ADCs reads. Due to 12-bit accuracy, the returned
        value ranges [0, 4095].

        :param int pin: individual or differential pin.
        :param bool is_differential: single-ended or differential read.

        .. note:: This library offers a helper class called `AnalogIn`_ for both single-ended
            and differential reads. If you opt to not implement `AnalogIn`_ during differential
            reads, then the ``pin`` parameter should be the first of the two pins associated with
            the desired differential channel mapping.
        """
        self._out_buf[0] = 0x40 | ((not is_differential) << 5) | (pin << 4)
        with self._spi_device as spi:
            # pylint: disable=no-member
            spi.write_readinto(self._out_buf, self._in_buf, out_end=2, in_end=2)
        return ((self._in_buf[0] & 0x0F) << 8) | self._in_buf[1]
