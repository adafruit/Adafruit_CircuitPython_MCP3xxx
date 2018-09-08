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

# create a mcp3004 object
#mcp = adafruit_mcp3xxx.MCP3004(spi,cs)

# create an an adc (single-ended) on pin 0
adc_single_ended = adafruit_mcp3xxx.AnalogIn(mcp, 1)
print('\nADC')
print('\tValue: ', adc_single_ended.value)
print('\tVolts: ', adc_single_ended.volts)

# create an an adc (differential) on pin 0
adc_diff = adafruit_mcp3xxx.AnalogIn_Differential(mcp, 0, 1)
print('\nDifferential ADC')
print('\tDiff. Value: ', adc_diff.value)
print('\tDiff. Voltage: ', adc_diff.volts)
