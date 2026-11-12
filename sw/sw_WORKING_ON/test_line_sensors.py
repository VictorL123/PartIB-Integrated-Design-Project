"""test_line_sensors.py - STEP 2: print what the sensors see. Robot on the table, pushed by hand.

Check: over the line the sensor shows 1 (if not, flip LINE_ON_VALUE in config.py);
moving the robot right of the line makes `error` go NEGATIVE (line is to its left).
"""
from utime import sleep
from line_sensors import LineSensors


def test_line_sensors():
    sensors = LineSensors()
    while True:
        print("raw", sensors.read(), "error", sensors.error(),
              "junction" if sensors.at_junction() else "")
        sleep(0.1)


if __name__ == "__main__":
    test_line_sensors()
