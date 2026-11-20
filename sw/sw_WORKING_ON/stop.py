from config import (LEFT_MOTOR_DIR, LEFT_MOTOR_PWM, RIGHT_MOTOR_DIR, RIGHT_MOTOR_PWM,
                    LEFT_MOTOR_INVERT, RIGHT_MOTOR_INVERT, require)
from motors import Motor, Drivetrain
from robot import Robot


def stop():
    #Stop the motors
    left = Motor(require("LEFT_MOTOR_DIR", LEFT_MOTOR_DIR),
                 require("LEFT_MOTOR_PWM", LEFT_MOTOR_PWM), LEFT_MOTOR_INVERT)
    right = Motor(require("RIGHT_MOTOR_DIR", RIGHT_MOTOR_DIR),
                  require("RIGHT_MOTOR_PWM", RIGHT_MOTOR_PWM), RIGHT_MOTOR_INVERT)
    drive = Drivetrain(left, right)
    drive.stop()

    #Turn off the lights
    robot = Robot()
    robot.lights.amber_off()
    robot.lights.green_off()
    robot.lights.red_off()

    #Stop the servos and reset them back to normal position
    """ ADD SERVO STOP CODE HERE """
    
    print("stopped")


if __name__ == "__main__":
    stop()
