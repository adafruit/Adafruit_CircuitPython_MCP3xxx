# SPDX-FileCopyrightText: 2018 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
:py:class:`~adafruit_mcp3xxx.adafruit_mcp3xxx.MCP3xxx`
============================================================

CircuitPython Library for MCP3xxx ADCs with SPI

* Author(s): ladyada, Brent Rubell, Kevin J. Walters

Implementation Notes
--------------------

**Hardware:**

* Adafruit `MCP3008 8-Channel 10-Bit ADC with SPI
  <https://www.adafruit.com/product/856>`_ (Product ID: 856)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

.. note:: The ADC chips' input pins (AKA "channels") are aliased in this library
    as integer variables whose names start with "P" (eg ``MCP3008.P0`` is channel 0 on the MCP3008
    chip). Each module that contains a driver class for a particular ADC chip has these aliases
    predefined accordingly. This is done for code readability and prevention of erroneous SPI
    commands.

.. important::
    The differential reads (comparisons done by the ADC chip) are limited to certain pairs of
    channels. These predefined pairs are referenced in this documentation as differential
    channel mappings. Please refer to the driver class of your ADC chip (`MCP3008`_,
    `MCP3004`_, `MCP3002`_) for a list of available differential channel mappings.
"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx.git"

from adafruit_bus_device.spi_device import SPIDevice

try:
    import typing  # pylint: disable=unused-import
    from digitalio import DigitalInOut
    from busio import SPI
except ImportError:
    pass


class MCP3xxx:
    """
    This abstract base class is meant to be inherited by `MCP3008`_, `MCP3004`_,
    or `MCP3002`_ child classes.

    :param ~adafruit_bus_device.spi_device.SPIDevice spi_bus: SPI bus the ADC is connected to.
    :param ~digitalio.DigitalInOut cs: Chip Select Pin.
    :param float ref_voltage: Voltage into (Vin) the ADC.
    :param int baudrate: the clock speed for communication to this SPI device. Defaults to 100k.
    """

    def __init__(
        self,
        spi_bus: SPI,
        cs: DigitalInOut,
        ref_voltage: float = 3.3,
        baudrate: int = 100_000,
    ):  # pylint: disable=invalid-name
        self._spi_device = SPIDevice(spi_bus, cs, baudrate=baudrate)
        self._out_buf = bytearray(3)
        self._in_buf = bytearray(3)
        self._ref_voltage = ref_voltage

        self._out_buf[0] = 0x01  # some sub-classes will overwrite this

    @property
    def reference_voltage(self) -> float:
        """Returns the MCP3xxx's reference voltage. (read-only)"""
        return self._ref_voltage
