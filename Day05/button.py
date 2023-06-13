import RPi.GPIO as GPIO
import time

button = 21
red = 17
green = 22
blue = 27
cnt = 0

def clickHandler(channel):
    global cnt
    cnt = cnt + 1
    
    print(cnt)

GPIO.setwarnings(False) # 의미없는 경고 로그 없애기
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button, GPIO.RISING, callback=clickHandler)

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.output(red, True)
GPIO.output(green, True)
GPIO.output(blue, True)

try:
    while True:
        
        if(cnt%8==1):
            GPIO.output(red, True)
            GPIO.output(green, True)
            GPIO.output(blue, True)
            time.sleep(1)

        if(cnt%8==2):
            GPIO.output(red, False)
            time.sleep(1)
            GPIO.output(red,True)

        if(cnt%8==3):
            GPIO.output(green, False)
            time.sleep(1)
            GPIO.output(green, True)

        if(cnt%8==4):
            GPIO.output(blue, False)
            time.sleep(1)
            GPIO.output(blue, True)

        if(cnt%8==5):
            GPIO.output(red, False)
            GPIO.output(green, False)
            GPIO.output(blue, True)
            time.sleep(1)

        if(cnt%8==6):
            GPIO.output(red, True)
            GPIO.output(green, False)
            GPIO.output(blue, False)
            time.sleep(1)

        if(cnt%8==7):
            GPIO.output(red, False)
            GPIO.output(green, True)
            GPIO.output(blue, False)
            time.sleep(1)

        if(cnt%8==0):
            GPIO.output(red, False)
            GPIO.output(green, False)
            GPIO.output(blue, False)
            time.sleep(1)
        

except KeyboardInterrupt:
    GPIO.cleanup()

