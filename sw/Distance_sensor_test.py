from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from utime import sleep

clockPin = 9
dataPin = 8

def test_vl53l0x():
    # configure I2C bus
    i2c_bus = I2C(id=0, sda=Pin(dataPin), scl=Pin(clockPin))
    
    #setup the vl53l0 object
    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)
    
    while True:
        print("Starting vl53l0...")
        vl53l0.start()
        
        #read 10 samples
        for independant in range(10):
            distance = vl53l0.read() - 30
            print(f"Distance = {distance}mm") #Check calibration here
            sleep(0.5)
        
        vl53l0.stop()

if __name__ == "__main__":
    test_vl53l0x()

