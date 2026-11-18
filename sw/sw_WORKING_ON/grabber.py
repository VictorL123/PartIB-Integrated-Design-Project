"""grabber.py - servo gripper + linear actuator lift.

The actuator has NO position feedback (the course example says so), so heights are
timed moves or limit-switch based. Rule from the brief: carried packages must be
<= 30 mm off the ground, and never rotated.
"""

from config import SERVO_HORIZONTAL_PIN, SERVO_VERTICAL_PIN
from servo import Servo


class Grabber:
    def __init__(self):
        """TODO: Servo on SERVO_PIN (course Servo class), actuator on ACTUATOR_DIR/PWM."""
        self.horizontal_servo = Servo(SERVO_HORIZONTAL_PIN)
        self.servo_vertical = Servo(SERVO_VERTICAL_PIN)
        
    def open(self):
        """TODO: servo to the open angle."""
        self.horizontal_servo.set_angle(130)

    def close(self):
        """TODO: servo to the closed angle (find an angle that grips without crushing)."""
        self.horizontal_servo.set_angle(60)        
        
    def raise_to(self, level):
        """TODO: level = "CARRY", "LOW_RACK" or "UPPER_RACK". Drive the actuator for a
        measured time, then stop. Always stop the actuator afterwards."""
        if level == "UPPER_RACK":
            self.servo_vertical.set_angle(30)

    def lower_to_ground(self):
        """Lower back to the ground when delivering to depot"""
        self.servo_vertical.set_angle(0)

    def package_present(self):
        """TODO: use DistanceSensor.package_near()."""
