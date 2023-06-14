# MQTT 패키지 설치 - paho-mqtt
# sudo pip install paho-mqtt
# 동시에 publish(데이터 송신[출판]) / subscribe (데이터 수신[구독])

from threading import Thread, Timer
import time
import json
import datetime as dt

import paho.mqtt.client as mqtt

# DHT11 온습도센서
import Adafruit_DHT as dht
#GPIO
import RPi.GPIO as GPIO

# GPIO, DHT 설정
sensor = dht.DHT11
rcv_pin = 10
green = 22
servo_pin = 18

GPIO.setwarnings(False)  # 오류메세지 제거
# green led init
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.output(green, GPIO.HIGH)   # True
# servo init
pwm = GPIO.PWM(servo_pin, 100)
pwm.start(3)    # 각도 0도 DutyCycle 3 ~ 20



# 데이터 보내는 객체
class publisher(Thread):
    def __init__(self):
        Thread.__init__(self)   # 스레드초기화
        self.host = '210.119.12.72' # 내 pc ip
        self.clientId = 'IOT72'
        self.count = 0
        self.port = 1883    # mqtt 기본 포트
        print('publisher 스레드 시작')
        self.client = mqtt.Client(self.clientId) # 설계대로?

    def run(self):
        self.client.connect(self.host, self.port)
        # self.client.username_pw_set() # id/pwd로 로그인할때 필요
        self.publish_data_auto()

    def publish_data_auto(self):
        humid, temp = dht.read_retry(sensor, rcv_pin)

        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 2023-06-14 10:39:10
        origin_data = { 'DEV_ID' : self.clientId,
                        'CURR_DT' : curr,
                        'TYPE' : 'HUMIDTEMP',
                        'STATE' : f'{temp} | {humid}' }    # data
        pub_data = json.dumps(origin_data)  # MQTT로 전송할 json 데이터로 변환
        self.client.publish(topic='pknu/rpi/control/', payload=pub_data)
        print(f'Data published #{self.count}')
        self.count += 1
        Timer(2.0, self.publish_data_auto).start()  # 2초마다 publish

# 받아오는 객체
class subscriber(Thread):
    def __init__(self): # 생성자
        Thread.__init__(self)
        self.host = '210.119.12.72' # Broker IP
        # self.host = "https://~~~~.com/~~~" 추후 aws azure 사용시 이런 식으로 사용
        self.port = 1883
        self.clientId = 'IOT72_SUB'
        self.topic = 'pknu/monitor/control/'
        print('subscriber 스레드 시작')
        self.client = mqtt.Client(client_id=self.clientId)

    def run(self):  # Thred.start() 함수를 실행하면 실행되는 함수
        self.client.on_connect = self.onConnect # 접속 성공 시그널 처리
        self.client.on_message = self.onMessage # 접속 후 메시지가 수신되면 처리
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic=self.topic)
        self.client.loop_forever()

    def onConnect(self, mqttc, obj, flags, rc):
        print(f'subscriber 연결됨 rc > {rc}')

    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        # print(f'{msg.topic} / {rcv_msg}')
        data = json.loads(rcv_msg)  # json data로 형변환
        state = data['STATE']
        print(f'현재 STATE : {state}')
        if (state == 'OPEN'):
            GPIO.output(green, GPIO.LOW)
            pwm.ChangeDutyCycle(12) # 90도
        elif (state == 'CLOSE'):
            GPIO.output(green, GPIO.HIGH)
            pwm.ChangeDutyCycle(3)  # 0도


        time.sleep(1.0)
0
if __name__ == '__main__':
    thPub = publisher() # 객체 생성
    thSub = subscriber()    # subscriber 객체 생성
    thPub.start()   # run() 자동 실행
    thSub.start()