import digitalio
import board
import busio
from adafruit_mcp3xxx.single_ended import MCP3008


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
adc = MCP3008(spi, cs)
r0 = adc[0].value
r0_volts = adc[0].volts
print('Raw ADC: ', r0)
print('Volts: ', r0_volts)
