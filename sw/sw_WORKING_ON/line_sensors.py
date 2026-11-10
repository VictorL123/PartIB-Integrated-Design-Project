"""line_sensors.py - turn raw sensor pins into the numbers the controller needs."""
from config import LINE_SENSOR_PINS, LINE_SENSOR_WEIGHTS, LINE_ON_VALUE, JUNCTION_CONFIRM
from machine import Pin

class LineSensors:
    def __init__(self):
        # TODO: create Pin.IN objects for LINE_SENSOR_PINS (think: pull-up or pull-down?)
        self._junction_count = 0

    def read(self):
        """TODO: return a list of 0/1, 1 = sees the line (use LINE_ON_VALUE)."""
        values = []
        for i in range(len(LINE_SENSOR_PINS)):
            sensor_pin = Pin(LINE_SENSOR_PINS[i], Pin.IN)
            if sensor_pin.value() == LINE_ON_VALUE:
                values.append(1)
            else:
                values.append(0)

        return values
    

    def error(self):
        """TODO: weighted position of the line. 
        Negative = line is left (speed up right), positive = line is right (speed up left).
        Return None if no sensor sees the line (lost)."""
        sensors = self.read()
        if sensors == [0,1,1,0]:
            error = 0
        elif sensors == [0,1,0,0]:
            error = -1
        elif sensors == [0,0,1,0]:
            error = 1
        elif sensors == [1,1,0,0]:
            error = -3
        elif sensors == [0,0,1,1]:
            error = 3
        elif sensors == [0,0,0,1]:
            error = 5
        elif sensors == [1,0,0,0]:
            error = -5
        elif sensors == [1,0,0,1]:
            error = None
        elif sensors == [0,0,0,0]:
            error = None
            raise Exception("no line found")
        elif sensors == [1,1,1,1] or sensors == [0,1,1,1] or sensors == [1,1,1,0]:
            self.at_junction()
        else:
            # 1011, 1101, 1001
            raise AssertionError("sensor condition does not support error")

        return error        


    def at_junction(self):
        """TODO: True only after the outer sensors have seen the line JUNCTION_CONFIRM
        readings IN A ROW. Reset the counter when they don't."""

    def centre_on_line(self):
        """TODO: used to know when a turn has found the line again."""
