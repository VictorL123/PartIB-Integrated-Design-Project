"""buttons.py - start/stop button (easily accessible per the brief)."""

from machine import Pin
from config import START_BUTTON_PIN

def start_pressed():
    """TODO: Pin on START_BUTTON_PIN (Pin.IN, PULL_DOWN as in the course example).
    Add debouncing."""
    # sits at vcc then goes to 0 when pressed, goes back to vcc when released
    buttonpin = Pin(START_BUTTON_PIN, Pin.IN)
    # follow rising or falling edge???, debouncing? 

def stop_pressed():
    """TODO: the stop must work from ANY state."""
