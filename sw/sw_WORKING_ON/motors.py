"""motors.py - wheel control.

Motor is the course class (sw/test_motor.py) plus set(): one number from -100 to 100.
Everything else in the project uses Drivetrain, never a raw Motor.
"""
from machine import Pin, PWM


class Motor:
    def __init__(self, dir_pin, pwm_pin, invert=False):
        self.mDir = Pin(dir_pin, Pin.OUT)      # direction pin
        self.pwm = PWM(Pin(pwm_pin))           # speed pin
        self.pwm.freq(1000)
        self.pwm.duty_u16(0)                   # start stopped
        self.invert = invert                   # for motors mounted mirror-image

    def off(self):
        self.pwm.duty_u16(0)

    def Forward(self, speed=100):
        self.mDir.value(0)                     # forward = 0, reverse = 1 on these drivers
        self.pwm.duty_u16(int(65535 * speed / 100))

    def Reverse(self, speed=30):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))

    def set(self, speed):
        """speed: -100 (full reverse) .. +100 (full forward). Applies `invert`."""
        if self.invert:
            speed = -speed
        speed = max(-100, min(100, speed))     # never exceed the valid range
        if speed > 0:
            self.Forward(speed)
        elif speed < 0:
            self.Reverse(-speed)
        else:
            self.off()


class Drivetrain:
    """Two motors treated as one vehicle."""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def drive(self, left_speed, right_speed):
        """Set both wheel speeds (-100..100). Different speeds make it steer."""
        self.left.set(left_speed)
        self.right.set(right_speed)

    def stop(self):
        """Both motors off. Always safe to call, even twice."""
        self.left.off()
        self.right.off()

    def spin(self, direction, speed):
        """Rotate on the spot. direction = "LEFT" (anticlockwise) or "RIGHT"."""
        if direction == "LEFT":
            self.drive(-speed, speed)
        else:
            self.drive(speed, -speed)
