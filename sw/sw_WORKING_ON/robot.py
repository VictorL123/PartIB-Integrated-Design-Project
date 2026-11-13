from config import (LEFT_MOTOR_DIR, LEFT_MOTOR_PWM, RIGHT_MOTOR_DIR, RIGHT_MOTOR_PWM,
                    LEFT_MOTOR_INVERT, RIGHT_MOTOR_INVERT, require)
from motors import Motor, Drivetrain
from line_sensors import LineSensors
from line_follow import LineFollower
from lights import Lights
from navigation import Route

class Robot:
    def __init__(self):
        left = Motor(require("LEFT_MOTOR_DIR", LEFT_MOTOR_DIR),
                     require("LEFT_MOTOR_PWM", LEFT_MOTOR_PWM), LEFT_MOTOR_INVERT)
        right = Motor(require("RIGHT_MOTOR_DIR", RIGHT_MOTOR_DIR),
                      require("RIGHT_MOTOR_PWM", RIGHT_MOTOR_PWM), RIGHT_MOTOR_INVERT)
        self.drive = Drivetrain(left, right)
        self.sensors = LineSensors()
        self.follower = LineFollower(self.drive,self.sensors)
        self.lights = Lights()
        self.navigate = Route()
