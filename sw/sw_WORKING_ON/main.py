from robot import Robot
from config import SPIN_SPEED
from utime import ticks_ms, ticks_diff, sleep_ms

robot = Robot()
while True:
    robot.drive.spin("LEFT", SPIN_SPEED)