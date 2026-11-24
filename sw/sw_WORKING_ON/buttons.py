"""buttons.py - start/stop button (easily accessible per the brief)."""

from machine import Pin
from time import sleep_ms

def start_pressed(stop_button):
    """TODO: Pin on START_BUTTON_PIN (Pin.IN, PULL_DOWN as in the course example).
    Add debouncing."""
    while stop_button.value() == 1:   # wait for press
        pass
    sleep_ms(20)                        # debounce press
    while stop_button.value() == 0:   # wait for release
        pass
    sleep_ms(20)                        # debounce release
    return True

def stop_pressed(stop_button):
    """TODO: the stop must work from ANY state."""
    return stop_button.value() == 0
