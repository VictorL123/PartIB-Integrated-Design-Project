"""magnet.py - decide north / south pole of the package.

Depends on the sensor you have: digital Hall (two pins?) or analogue (ADC).
If analogue: record the no-magnet reading at startup, then the SIGN of (reading - rest)
gives N or S. Print raw values with real blocks before writing the thresholds.
"""
from config import HALL_PIN, HALL_LOWER_THREASHOLD, HALL_UPPER_THREASHOLD
from machine import Pin, ADC
from utime import sleep_ms


def read_polarity():
    """Returns "N", "S" or None (no clear field). Averaged over a few samples. CHECK THE DAMN THRESHOLDS!!!!!!!!"""
    #Define the hall effect sensors' input pin 
    return None
    magnet_sensor = ADC(Pin(HALL_PIN))
    v_total = 0

    #For 20 readings convert to a voltage then sum them 
    for readings in range(20):
        reading = magnet_sensor.read_u16()
        v_out = reading * (3.3 / 65535)
        v_total += v_out
        sleep_ms(20)

    #Average those readings and check those
    v_average = v_total / 20

    #Now we check the v_average againt our threasholds
    if v_average > HALL_UPPER_THREASHOLD:
        return "N"
    elif v_average < HALL_LOWER_THREASHOLD:
        return "S"
    else: 
        return None

