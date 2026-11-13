"""distance.py - thin wrapper around the course VL53L0X driver.

Import path: from libs.VL53L0X.VL53L0X import VL53L0X
Course setup (see sw/test_vl53l0x.py): I2C(id=0, sda=Pin(8), scl=Pin(9)), then
set_Vcsel_pulse_period(type[0], 18) and (type[1], 14), then start() once, read() returns mm.
"""

# distance sensor for safety??????????

from config import PACKAGE_NEAR_MM, I2C_ID, I2C_SDA, I2C_SCL
from libs.VL53L0X.VL53L0X import VL53L0X
from machine import Pin, I2C
from utime import sleep

class DistanceSensor:
    def __init__(self):
        """TODO: set up I2C + driver as above, call start() once (continuous mode)."""
        # config I2C Bus
        self.i2c_bus = I2C(id=I2C_ID, sda=Pin(I2C_SDA), scl=Pin( I2C_SCL)) # I2C0 on GP8 & GP9
        # print(i2c_bus.scan())  # Get the address (nb 41=0x29, 82=0x52)
        
        # Setup vl53l0 object
        self.vl53l0 = VL53L0X(self.i2c_bus)
        self.vl53l0.set_Vcsel_pulse_period(self.vl53l0.vcsel_period_type[0], 18)
        self.vl53l0.set_Vcsel_pulse_period(self.vl53l0.vcsel_period_type[1], 14)
    
    
        print("Starting vl53l0...")

        # Start device
        self.vl53l0.start()

        # # Read ten samples
        # for _ in range(10):
        #     distance = self.vl53l0.read()
        #     print(f"Distance = {distance}mm")  # Check calibration!
        #     sleep(0.5)
        
        # # Stop device
        # self.vl53l0.stop()

    def mm(self):
        """TODO: return distance in mm, or None if the read fails or the reading means
        'nothing in range' (the driver returns ~8190 then). Wrap in try/except."""
        try:
            distance = self.vl53l0.read() - 30
            print(f"Distance = {distance}mm")  # Check calibration!

        except:
            print("No valid reading")
            return None

    def package_near(self):
        """TODO: True if mm() is not None an.d below PACKAGE_NEAR_MM."""
