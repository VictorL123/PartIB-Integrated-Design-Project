"""lights.py - amber flasher, red/green polarity indicator.

Remember: LEDs go through an optical isolator, never straight off the Pico pin.
Use machine.Timer for the flashing so it never blocks the control loop.
Check the brief: steady amber when powered, flashing when moving, and OFF in the
start area for the scoring - ask a demonstrator how to reconcile these.
"""

from machine import Pin
from utime import sleep
from config import AMBER_PIN, RED_PIN, GREEN_PIN, LED_ON_VALUE, LED_OFF_VALUE, FLASH_HZ    

class Lights:
    def __init__(self):
        """Pin.OUT for amber, red, green """
        self.red = Pin(RED_PIN, Pin.OUT)
        self.amber = Pin(AMBER_PIN, Pin.OUT)
        self.green = Pin(GREEN_PIN, Pin.OUT)

    # functions for lights on/off
    def amber_on(self):
        self.amber.value(LED_ON_VALUE)

    def amber_off(self):
        self.amber.value(LED_OFF_VALUE)

    def green_on(self):
        self.green.value(LED_ON_VALUE)

    def green_off(self):
        self.green.value(LED_OFF_VALUE)

    def red_on(self):
        self.red.value(LED_ON_VALUE)

    def red_off(self):
        self.red.value(LED_OFF_VALUE)

    def amber_flash(self, elapsed):
        led_on = ((elapsed // 1000) % 2 == 0)
        if led_on:
            self.amber_on()
        else:
            self.amber_off()

    def red_green_test(self, elapsed):
        """A funtion to flash the red and green LEDs on and off for a test, using the floor division operator //"""
        flash_when = ((elapsed // 1000) % 2)
        if flash_when == 0:
            self.red_on()
            self.green_on()
        else:
            self.red_off()
            self.green_off()

    def show_polarity(self, polarity):
        """ "N" -> red steady, "S" -> green steady, None -> both off. """
        if polarity == "N":
            self.red_on()
            self.green_off()

        elif polarity == "S":
            self.red_off()
            self.green_on()

        elif polarity == None:
            self.red_off()
            self.green_off()

        else:
            #Faliure state, if this occurs something is wrong and panic should ensue
            self.red_on()
            self.green_on()
            print("Error in the polarity function, the result was not one of 'N', 'S', or None")
