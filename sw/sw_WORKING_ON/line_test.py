from robot import Robot
from config import BASE_SPEED
from utime import ticks_ms, ticks_diff, sleep_ms

robot = Robot()
while True:
    robot.follower.step(BASE_SPEED)
              