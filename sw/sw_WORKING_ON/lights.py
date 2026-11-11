"""lights.py - amber flasher, red/green polarity indicator.

Remember: LEDs go through an optical isolator, never straight off the Pico pin.
Use machine.Timer for the flashing so it never blocks the control loop.
Check the brief: steady amber when powered, flashing when moving, and OFF in the
start area for the scoring - ask a demonstrator how to reconcile these.
"""

from machine import Pin
from utime import sleep
from config import AMBER_PIN, RED_PIN, GREEN_PIN, LED_ON_VALUE, FLASH_HZ    

class Lights:
    def __init__(self):
        """TODO: Pin.OUT for amber, red, green; a Timer object for flashing."""
        self.red = Pin(RED_PIN, Pin.OUT)
        self.amber = Pin(AMBER_PIN, Pin.OUT)
        self.green = Pin(GREEN_PIN, Pin.OUT)

    def amber_on(self):
        """TODO"""
        self.amber.value(LED_ON_VALUE)


    def amber_flash(self, on):
        """TODO: start or stop the periodic toggle at FLASH_HZ."""
        print("Flashing LED")
        # is this just never goint to stop???
        while on:
            self.amber_on()
            sleep(1/FLASH_HZ)
            self.amber_off()
            sleep(1/FLASH_HZ)
        self.amber_off()
        

    def amber_off(self):
        """TODO"""
        self.amber.value(0)



    def show_polarity(self, polarity):
        """TODO: "N" -> red steady, "S" -> green steady, None -> both off."""
