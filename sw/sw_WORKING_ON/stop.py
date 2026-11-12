from config import (LEFT_MOTOR_DIR, LEFT_MOTOR_PWM, RIGHT_MOTOR_DIR, RIGHT_MOTOR_PWM,
                    LEFT_MOTOR_INVERT, RIGHT_MOTOR_INVERT, require)
from motors import Motor, Drivetrain


def stop():
    left = Motor(require("LEFT_MOTOR_DIR", LEFT_MOTOR_DIR),
                 require("LEFT_MOTOR_PWM", LEFT_MOTOR_PWM), LEFT_MOTOR_INVERT)
    right = Motor(require("RIGHT_MOTOR_DIR", RIGHT_MOTOR_DIR),
                  require("RIGHT_MOTOR_PWM", RIGHT_MOTOR_PWM), RIGHT_MOTOR_INVERT)
    drive = Drivetrain(left, right)
    drive.stop()
    print("stopped")


if __name__ == "__main__":
    stop()
