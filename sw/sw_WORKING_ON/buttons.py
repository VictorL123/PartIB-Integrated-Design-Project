"""buttons.py - start/stop button (easily accessible per the brief)."""

from machine import Pin
from config import START_BUTTON_PIN

def start_pressed(stop_button):
    """TODO: Pin on START_BUTTON_PIN (Pin.IN, PULL_DOWN as in the course example).
    Add debouncing."""
    # sits at vcc then goes to 0 when pressed, goes back to vcc when released
    # follow rising or falling edge???, debouncing? 
    start = 1
    while start == 1:
        # Poll the value
        start = stop_button.value()
    return True

def stop_pressed(stop_button):
    """TODO: the stop must work from ANY state."""
    if stop_button.value() == 0:
        return True
