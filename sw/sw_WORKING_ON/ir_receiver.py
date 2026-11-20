"""ir_receiver.py - the traffic light sends an IR signal with the green light.

Unknown: the exact signal format. Start by printing what the receiver pin does
(like test_input.py) when the light goes green, then decide how to detect it.
"""
from config import IR_PIN, IR_THREASHOLD
from machine import Pin, ADC
from utime import sleep_ms
from robot import Robot
from lights import Lights


def wait_for_green(timeout_ms=5):
    """ Looks for the IR pulse from the green light, and then returns True when it's seen the pulse, and a False otherwise """
    #Set up the IR sensor and read the contents of the pin
    IR_sensor = ADC(Pin(IR_PIN))
    input_value = IR_sensor.read_u16()
    robot = Robot()
    v_total = 0

    #For 20 readings convert to a voltage then sum them 
    for readings in range(10):
        reading = IR_sensor.read_u16()
        v_out = reading * (3.3 / 65535)
        v_total += v_out
        sleep_ms(20)

    v_average = v_total / 10
    print(v_average)

    if v_average < IR_THREASHOLD:
        #If it sees the green light pulse, then it returns true and breaks the loop and flashes green to show me for testing
        #robot.lights.green_on()
        #sleep_ms(1000)
        #robot.lights.green_off() #Test code
        return True

    else:
        #If the light is still red, then loop inside this function by going back and getting a new reading
        sleep_ms(timeout_ms)
        print("redddd")
        return False


