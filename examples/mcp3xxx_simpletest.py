import digitalio
import board
import busio
from adafruit_mcp3xxx.single_ended import MCP3008


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
adc = MCP3008(spi, cs)
print(adc[0].value)