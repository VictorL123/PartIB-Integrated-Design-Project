from machine import Pin, PWM
from utime import sleep

class Drive:
    #Take the input pins of both motors and allow them to drive together as one system
    def __init__(self, directionPin1, PWMPin1, directionPin2, PWMPin2): #PWM = pulse-width modulation and describes inputing a square wave to lower average pin volatage
        self.