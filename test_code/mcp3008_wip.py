import busio
import digitalio
import board

cs = digitalio.DigitalInOut(board.D5)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
while not spi.try_lock():
    pass
spi.configure(baudrate=1000000, phase=0, polarity=0)

# 0 = differential, 1 = single
adc_mode = 1 
# 0 thru 7
adc_channel = 0

out_buf = bytearray(3)
in_buf = bytearray(3)

# command
command = (0x01 << 7)
command |= (adc_mode << 6)
command |= ((adc_channel & 0x07) << 3)
out_buf[0] = command
out_buf[1] = 0x00
out_buf[2] = 0x00

#dbg 
print('out buffer: ', out_buf)
print('in buffer: ', in_buf)

# begin spi
cs.value = False

spi.write_readinto(out_buf, in_buf,out_start=0, out_end=len(out_buf), in_start=0, in_end=len(in_buf))

# end transaction
cs.value = True 
spi.unlock()

print('rcv. from adc: ', in_buf)

# response data, 10b
result = (in_buf[0] & 0x01) << 9
result |= (in_buf[1] & 0xFF) << 1
result |= (in_buf[2] & 0x80) >> 7
result &= 0x3FF
print ('result  ', result)

    