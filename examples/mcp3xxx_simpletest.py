import busio
import digitalio
import board
from adafruit_mcp3xxx import adafruit_mcp3xxx

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object (mcp3008 type)
mcp = adafruit_mcp3xxx.MCP3008(spi,cs)

print(mcp)

