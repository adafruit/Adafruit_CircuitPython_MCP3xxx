import adafruit_mcp3xxx
from busio import SPI
import digitalio
from digitalio import DigitalInOut
import board

spi = SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp3008 object
mcp = adafruit_mcp3xxx.MCP3008(spi, cs)

# read mcp, ch0 raw value
print(mcp.adc_value(0))

# read mcp, ch0 voltage value 
print(mcp.adc_volts(0))