"""lights.py - amber flasher, red/green polarity indicator.

Remember: LEDs go through an optical isolator, never straight off the Pico pin.
Use machine.Timer for the flashing so it never blocks the control loop.
Check the brief: steady amber when powered, flashing when moving, and OFF in the
start area for the scoring - ask a demonstrator how to reconcile these.
"""


class Lights:
    def __init__(self):
        """TODO: Pin.OUT for amber, red, green; a Timer object for flashing."""

    def amber_flash(self, on):
        """TODO: start or stop the periodic toggle at FLASH_HZ."""

    def amber_off(self):
        """TODO"""

    def show_polarity(self, polarity):
        """TODO: "N" -> red steady, "S" -> green steady, None -> both off."""
