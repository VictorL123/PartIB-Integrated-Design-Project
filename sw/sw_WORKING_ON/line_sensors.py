"""line_sensors.py - turn raw sensor pins into the numbers the controller needs."""
from config import LINE_SENSOR_PINS, LINE_SENSOR_WEIGHTS, LINE_ON_VALUE, JUNCTION_CONFIRM
from machine import Pin


class LineSensors:
    def __init__(self):
        # TODO: create Pin.IN objects for LINE_SENSOR_PINS (think: pull-up or pull-down?)
        self._junction_count = 0

    def read(self):
        """ Read the sensors, return list of 0/1 left to right, 1 = sees line
        TODO: return a list of 0/1, 1 = sees the line (use LINE_ON_VALUE)."""
        # initialise list
        values = []
        # get data for each pin
        for i in range(len(LINE_SENSOR_PINS)):
            # set pin
            sensor_pin = Pin(LINE_SENSOR_PINS[i], Pin.IN)
            # check if on line and add values to list
            if sensor_pin.value() == LINE_ON_VALUE:
                values.append(1)
            else:
                values.append(0)

        return values
    

    def error(self):
        """TODO: weighted position of the line. 
        Negative = line is left (speed up right), positive = line is right (speed up left).
        Return None if no sensor sees the line (lost)."""
        # read sensors
        sensors = self.read()
        #  set error
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
        elif sensors == [1,0,0,1] or sensors == [0,0,0,0]:
            error = None
        elif sensors == [1,1,1,1] or sensors == [0,1,1,1] or sensors == [1,1,1,0]:
            # at junction
            error = 0
        else:
            # other conditions: 1011, 1101, 1001
            raise AssertionError("sensor condition does not support error")

        return error        


    def at_junction(self):
        """TODO: True only after the outer sensors have seen the line JUNCTION_CONFIRM
        readings IN A ROW. Reset the counter when they don't."""
        # read values
        values = self.read()
        # this may not work for corners that are not t junctions of the robot does not enter on line
        if (values[0] or values[-1]) and (values[1] and values[2]):
            self._junction_count += 1
        else:
            self._junction_count = 0
        return self._junction_count >= JUNCTION_CONFIRM

    def centre_on_line(self):
        """TODO: used to know when a turn has found the line again."""
