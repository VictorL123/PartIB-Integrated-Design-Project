"""motors.py - wheel control.

Start from the course Motor class in sw/test_motor.py (Forward/Reverse/off).
Do NOT import test_motor directly if it runs code at import: copy the class here.
"""

class Motor:
    """One motor: a direction pin and a PWM pin.
    TODO: copy the course Motor class, then add set(speed) taking -100..100
    (positive = forward, which is dir 0 on these drivers)."""

    def __init__(self, dir_pin, pwm_pin):
        raise NotImplementedError

    def set(self, speed):
        raise NotImplementedError


class Drivetrain:
    """Two motors treated as one vehicle. The rest of the code only uses this."""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def drive(self, left_speed, right_speed):
        """TODO: set both motors. Clamp to -100..100."""

    def stop(self):
        """TODO: both motors off. Must always be safe to call."""

    def spin(self, direction, speed):
        """TODO: rotate on the spot. direction = "LEFT" or "RIGHT"."""
