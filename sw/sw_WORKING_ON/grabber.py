"""grabber.py - servo gripper + linear actuator lift.

The actuator has NO position feedback (the course example says so), so heights are
timed moves or limit-switch based. Rule from the brief: carried packages must be
<= 30 mm off the ground, and never rotated.
"""


class Grabber:
    def __init__(self):
        """TODO: Servo on SERVO_PIN (course Servo class), actuator on ACTUATOR_DIR/PWM."""

    def open(self):
        """TODO: servo to the open angle."""

    def close(self):
        """TODO: servo to the closed angle (find an angle that grips without crushing)."""

    def raise_to(self, level):
        """TODO: level = "CARRY", "LOW_RACK" or "UPPER_RACK". Drive the actuator for a
        measured time, then stop. Always stop the actuator afterwards."""

    def package_present(self):
        """TODO: use DistanceSensor.package_near()."""
