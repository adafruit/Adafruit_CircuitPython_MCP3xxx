import busio
import digitalio
import board
from adafruit_mcp3xxx.mcp3004 import MCP3004
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object from MCP3004 class
mcp = MCP3004(spi, cs)

# create a differential analog input channel;
chan = AnalogIn(mcp, MCP3004.pin_2)

print('Raw ADC Value: ', chan.value)
print('Voltage: ' + str(chan.voltage) + 'V')
