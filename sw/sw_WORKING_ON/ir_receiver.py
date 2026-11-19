"""ir_receiver.py - the traffic light sends an IR signal with the green light.

Unknown: the exact signal format. Start by printing what the receiver pin does
(like test_input.py) when the light goes green, then decide how to detect it.
"""
from config import IR_PIN, IR_THREASHOLD
from machine import Pin, ADC


def wait_for_green(timeout_ms=None):
    """ Looks for the IR pulse from the green light, and then returns True when it's seen the pulse, and a False otherwise """
    #Set up the IR sensor and read the contents of the pin
    IR_sensor = ADC(Pin(IR_PIN))
    input_value = IR_sensor.read_u16()

    #Convert from the raw input into voltage
    v_out = input_value * (3.3 / 65535) 

    

