"""distance.py - thin wrapper around the course VL53L0X driver.

Import path: from libs.VL53L0X.VL53L0X import VL53L0X
Course setup (see sw/test_vl53l0x.py): I2C(id=0, sda=Pin(8), scl=Pin(9)), then
set_Vcsel_pulse_period(type[0], 18) and (type[1], 14), then start() once, read() returns mm.
"""

# distance sensor for safety??????????

from config import PACKAGE_NEAR_MM


class DistanceSensor:
    def __init__(self):
        """TODO: set up I2C + driver as above, call start() once (continuous mode)."""

    def mm(self):
        """TODO: return distance in mm, or None if the read fails or the reading means
        'nothing in range' (the driver returns ~8190 then). Wrap in try/except."""

    def package_near(self):
        """TODO: True if mm() is not None and below PACKAGE_NEAR_MM."""
