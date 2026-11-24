"""grabber.py - servo gripper + linear actuator lift.

The actuator has NO position feedback (the course example says so), so heights are
timed moves or limit-switch based. Rule from the brief: carried packages must be
<= 30 mm off the ground, and never rotated.
"""

from config import SERVO_HORIZONTAL_PIN, SERVO_VERTICAL_PIN, SERVO_HOR_START_ANGLE, SERVO_VER_START_ANGLE, VER_TOP_ANGLE, HOR_CLOSED_ANGLE, HOR_OPEN_ANGLE, HOR_SPEED_DEG_S, VER_SPEED_DEG_S, VER_BOTTOM_RACK_ANGLE
from servo import Servo, SlowServo


class Grabber:
    def __init__(self):
        """Servos on SERVO_HORIZONTAL_PIN and SERVO_VERTICAL_PIN"""
        self.horizontal_servo = SlowServo(SERVO_HORIZONTAL_PIN, SERVO_HOR_START_ANGLE)
        self.servo_vertical = SlowServo(SERVO_VERTICAL_PIN, SERVO_VER_START_ANGLE)
        
    def open(self):
        """servo to the open angle."""
        self.horizontal_servo.move_to(HOR_OPEN_ANGLE, HOR_SPEED_DEG_S)

    def close(self):
        """Servo to the closed angle - test angle that grips without crushing."""
        self.horizontal_servo.move_to(HOR_CLOSED_ANGLE, HOR_SPEED_DEG_S)
        
    def raise_before_grab(self, level):
        """ sets height of grabber for collection - needs calibrating"""
        if level == "top":
            self.servo_vertical.move_to(SERVO_VER_START_ANGLE, VER_SPEED_DEG_S)
        elif level == "low":
            self.servo_vertical.move_to(VER_BOTTOM_RACK_ANGLE, VER_SPEED_DEG_S)

    def pick_up(self):
        """sets carry height - needs calibrating"""
        self.servo_vertical.move_to(VER_TOP_ANGLE, VER_SPEED_DEG_S)

    def lower_to_ground(self):
        """Lower back to the ground when delivering to depot"""
        self.servo_vertical.move_to(SERVO_VER_START_ANGLE, VER_SPEED_DEG_S)

    def package_present(self):
        """TODO: use DistanceSensor.package_near() or servo feedback??? distance sensor not acurate within distance of box"""


def test_grabber():
    grabber = Grabber()
    grabber.open()
    grabber.close()
    grabber.raise_before_grab("top")
    grabber.pick_up()
    grabber.lower_to_ground()
    
    
# Uncomment to run
    
#test_grabber()