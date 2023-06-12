# LED 깜빡
import RPi.GPIO as GPIO
import time

signal_pin = 18

# GPIO.setmode(GPIO.BOARD)    # 1~40
GPIO.setmode(GPIO.BCM)      # GPIO 28, GND
GPIO.setup(signal_pin, GPIO.OUT)    # GPIO 18번 핀 출력

while(True):
    GPIO.output(signal_pin, True)   # GPIO18번 핀에 전압시그널 온
    time.sleep(0.1)   # 2초동안 불켜짐
    GPIO.output(signal_pin, False)  # GPIO18번 핀 오프
    time.sleep(0.1)   # 1초 꺼짐