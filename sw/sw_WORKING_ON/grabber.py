"""grabber.py - servo gripper + linear actuator lift.

The actuator has NO position feedback (the course example says so), so heights are
timed moves or limit-switch based. Rule from the brief: carried packages must be
<= 30 mm off the ground, and never rotated.
"""

from config import SERVO_HORIZONTAL_PIN, SERVO_VERTICAL_PIN
from servo import Servo


class Grabber:
    def __init__(self):
        """Servos on SERVO_HORIZONTAL_PIN and SERVO_VERTICAL_PIN"""
        self.horizontal_servo = Servo(SERVO_HORIZONTAL_PIN)
        self.servo_vertical = Servo(SERVO_VERTICAL_PIN)
        
    def open(self):
        """servo to the open angle."""
        self.horizontal_servo.set_angle(95)

    def close(self):
        """TODO: Servo to the closed angle - test angle that grips without crushing."""
        self.horizontal_servo.set_angle(10)
        
    def raise_to(self, level):
        """ TODO: sets height of grabber for collection - needs calibrating"""
        if level == "top":
            self.servo_vertical.set_angle(30)
        elif level == "low":
            self.servo_vertical.set_angle(0)

    def pick_up(self):
        """TODO: sets carry height - needs calibrating"""
        self.servo_vertical.set_angle(40)

    def lower_to_ground(self):
        """Lower back to the ground when delivering to depot"""
        self.servo_vertical.set_angle(0)

    def package_present(self):
        """TODO: use DistanceSensor.package_near() or servo feedback??? distance sensor not acurate within distance of box"""
