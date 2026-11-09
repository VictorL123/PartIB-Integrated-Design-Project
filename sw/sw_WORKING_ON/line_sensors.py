"""line_sensors.py - turn raw sensor pins into the numbers the controller needs."""
from config import LINE_SENSOR_PINS, LINE_SENSOR_WEIGHTS, LINE_ON_VALUE, JUNCTION_CONFIRM


class LineSensors:
    def __init__(self):
        # TODO: create Pin.IN objects for LINE_SENSOR_PINS (think: pull-up or pull-down?)
        self._junction_count = 0

    def read(self):
        """TODO: return a list of 0/1, 1 = sees the line (use LINE_ON_VALUE)."""

    def error(self):
        """TODO: weighted position of the line. Negative = line is left, positive = right.
        Return None if no sensor sees the line (lost)."""

    def at_junction(self):
        """TODO: True only after the outer sensors have seen the line JUNCTION_CONFIRM
        readings IN A ROW. Reset the counter when they don't."""

    def centre_on_line(self):
        """TODO: used to know when a turn has found the line again."""
