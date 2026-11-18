from distance import DistanceSensor
from utime import sleep_ms

distance_sensor = DistanceSensor()
for i in range(100):
    distance_sensor.mm()
    sleep_ms(1000)