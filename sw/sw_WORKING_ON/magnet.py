"""magnet.py - decide north / south pole of the package.

Depends on the sensor you have: digital Hall (two pins?) or analogue (ADC).
If analogue: record the no-magnet reading at startup, then the SIGN of (reading - rest)
gives N or S. Print raw values with real blocks before writing the thresholds.
"""
from config import HALL_PIN, HALL_LOWER_THREASHOLD, HALL_UPPER_THREASHOLD
from machine import Pin, ADC
from utime import sleep_ms
from robot import Robot


def read_polarity():
    """Returns "N", "S" or None (no clear field). Averaged over a few samples. CHECK THE DAMN THRESHOLDS!!!!!!!!"""
    #Define the hall effect sensors' input pin 
    magnet_sensor = ADC(Pin(HALL_PIN))
    v_total = 0

    #For 20 readings convert to a voltage then sum them 
    for readings in range(20):
        reading = magnet_sensor.read_u16()
        v_out = reading * (3/ 65535)
        v_total += v_out
        sleep_ms(20)

    #Average those readings and check those
    v_average = v_total / 20
    print(v_average)

    #Now we check the v_average againt our threasholds
    if v_average > HALL_UPPER_THREASHOLD:
        return "N"
    elif v_average < HALL_LOWER_THREASHOLD:
        return "S"
    else: 
        return None

def read_polarity_fake():
    return "N"

def test_hall_effect():
    #Read the polarity and find the robot
    while True:
        polarity = read_polarity()
    #robot = Robot()

    #Print out what the polarity was and light up the lights (test this too)
    #robot.grabber.raise_before_grab("low")
    #robot.grabber.open()
        print(polarity)
    #robot.lights.show_polarity(polarity)

        sleep_ms(300)
    #robot.grabber.lower_to_ground()
    #robot.grabber.close()

#test_hall_effect()