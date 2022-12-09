import RPi.GPIO as GPIO
import smbus
import random
from time import sleep

GPIO.setmode(GPIO.BCM)

## i2c
i2c = smbus.SMBus(1)
addr = 0x48 # $ i2cdetect -y 1

## GPIO pin
# LF = 21
# LB = 22
# RF = 23
# RB = 24

# GPIO.setmode(GPIO.BOARD)

# GPIO.setup(LF, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(LB, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(RF, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(RB, GPIO.OUT, initial=GPIO.LOW)

# GPIO.output(LF, GPIO.LOW)
# GPIO.output(LB, GPIO.LOW)
# GPIO.output(RF, GPIO.LOW)
# GPIO.output(RB, GPIO.LOW)

def main():
    # GPIO.output(LF, GPIO.HIGH)
    # GPIO.output(RF, GPIO.HIGH)
    while(1):
        data = []
        value = random.randint(0, 255)
        data.append(value)
        print("write_data: {}".format(value))
#        data00 = int((value % 16) << 4)
#        data01 = int(value // 16)
#        i2c.write_i2c_block_data(addr, 0x40, [data00, data01])
#        print(hex(data01) + ", " + hex(data00))
#        i2c.write_i2c_block_data(addr, 0x42, data)
        print("read_data: {}".format(i2c.read_byte(addr)))
        i2c.write_byte_data(addr, 0x42, value)
        sleep(5)

# def remove():
#     GPIO.output(LF, GPIO.LOW)
#     GPIO.output(LB, GPIO.LOW)
#     GPIO.output(RF, GPIO.LOW)
#     GPIO.output(RB, GPIO.LOW)
#     GPIO.cleanup()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
#        print(type(e))
#        print(e)
        # remove()
        print("bye")
        i2c.write_byte_data(addr, 0x42, 0x00)
