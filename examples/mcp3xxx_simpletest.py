import busio
import digitalio
import board
from adafruit_mcp3xxx import adafruit_mcp3xxx

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create a mcp3008 object
mcp = adafruit_mcp3xxx.MCP3008(spi,cs)

# create an an adc object on pin 0
adc0 = adafruit_mcp3xxx.AnalogIn(mcp, 0)

print(adc0.value)
print(adc0.volts)
