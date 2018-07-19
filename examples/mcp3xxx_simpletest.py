#####
import busio
import digitalio
import board
from adafruit_mcp3xxx import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object (mcp3008 type)
mcp = MCP3008(spi,cs)

print(mcp)

