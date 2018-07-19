import digitalio
import board
import time
import busio
from adafruit_mcp3xxx.single_ended import MCP3008

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create an ADC object on Pin 0
adc_0 = MCP3008(0, spi, cs)
print("\nADC Pin 0:")
print('\traw value: ', adc_0.pin.value)
print('\tvoltage: ', adc_0.pin.volts, 'V')

# create an ADC object on Pin 1
adc_1 = MCP3008(1, spi, cs)
print("\nADC Pin 1:")
print('\traw value: ', adc_1.pin.value)
print('\tvoltage: ', adc_1.pin.volts, 'V')