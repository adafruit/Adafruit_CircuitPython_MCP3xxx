import busio
import digitalio
import board
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.differential_analog_in import DifferentialAnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object from MCP3008 class
mcp = MCP3008(spi, cs)

# create a differential analog input channel with pin 0 and pin 1
chan = DifferentialAnalogIn(mcp, MCP3008.pin_0, MCP3008.pin_1)

print('Differential ADC Value: ', chan.value)
print('Differential ADC Voltage: ' + str(chan.voltage) + 'V')
