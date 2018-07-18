import adafruit_mcp3xxx
from busio import SPI
import digitalio
from digitalio import DigitalInOut
import board

spi = SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp3008 object
mcp = adafruit_mcp3xxx.MCP3008(spi, cs)

"""
Single-Ended Read
"""
# channel 0 raw value
print('CH0 Value: ', mcp.read_adc(0))
# channel 0 voltage value 
print('CH0 Voltage:', mcp.read_volts(0), 'volts')

"""
Differential Read
"""
# differential 0 raw value
print('differential 0 (CH0-CH1) value:', mcp.read_adc_difference(0))
# differential 0 differential voltage
print('differential 0 (CH0-CH1) value:', mcp.read_volts_difference(0))
