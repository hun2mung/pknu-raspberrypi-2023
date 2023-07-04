# OpenCV 테스트
import cv2
from picamera2 import Picamera2
import datetime 

cam = Picamera2()
cam.preview_configuration.main.size=(800,600)
cam.preview_configuration.main.format='RGB888'
cam.preview_configuration.align()

cam.configure('preview')
cam.start()


while True:
    frame = cam.capture_array()
    cv2.imshow('piCam', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()