# 온습도센서 DHT11
import Adafruit_DHT as dht
import time

sensor = dht.DHT11
rcv_pin = 10

try:
    while(True):
        humid, temp = dht.read_retry(sensor, rcv_pin)
        if humid is not None and temp is not None:
            print(f'온도 : {temp} / 습도 : {humid}%')
        else:
            print('센싱에러')
        time.sleep(1)
except Exception as ex:
    print(ex)
finally:
    print('종료')