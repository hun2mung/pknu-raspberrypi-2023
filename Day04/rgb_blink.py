import RPi.GPIO as GPIO
import time

red = 17
green = 22
blue = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

try:
    while True:
        GPIO.output(red, True)
        time.sleep(1)
        GPIO.output(red,False)

        GPIO.output(blue, True)
        time.sleep(1)
        GPIO.output(blue,False)

        GPIO.output(green, True)
        time.sleep(1)
        GPIO.output(green,False)

except KeyboardInterrupt:
    GPIO.cleanup()

