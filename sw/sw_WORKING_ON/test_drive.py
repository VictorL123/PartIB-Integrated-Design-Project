"""test_drive.py - STEP 1: check both wheels, with the robot LIFTED OFF THE TABLE.

Each wheel should spin FORWARD first. If one spins backwards, set that motor's
INVERT flag in config.py (do not rewire). Then check the spins turn the right way.
"""
from utime import sleep
from config import (LEFT_MOTOR_DIR, LEFT_MOTOR_PWM, RIGHT_MOTOR_DIR, RIGHT_MOTOR_PWM,
                    LEFT_MOTOR_INVERT, RIGHT_MOTOR_INVERT, require)
from motors import Motor, Drivetrain


def test_drive():
    left = Motor(require("LEFT_MOTOR_DIR", LEFT_MOTOR_DIR),
                 require("LEFT_MOTOR_PWM", LEFT_MOTOR_PWM), LEFT_MOTOR_INVERT)
    right = Motor(require("RIGHT_MOTOR_DIR", RIGHT_MOTOR_DIR),
                  require("RIGHT_MOTOR_PWM", RIGHT_MOTOR_PWM), RIGHT_MOTOR_INVERT)
    drive = Drivetrain(left, right)
    try:
        print("left wheel forward");  left.set(40);  sleep(1.5);  left.set(0)
        print("right wheel forward"); right.set(40); sleep(1.5);  right.set(0)
        print("both forward");        drive.drive(40, 40);        sleep(1.5)
        print("spin LEFT (anticlockwise from above)"); drive.spin("LEFT", 40);  sleep(1.5)
        print("spin RIGHT");          drive.spin("RIGHT", 40);    sleep(1.5)
    finally:
        drive.stop()
        print("stopped")


if __name__ == "__main__":
    test_drive()
