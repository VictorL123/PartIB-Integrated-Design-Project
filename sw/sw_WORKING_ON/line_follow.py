"""line_follow.py - the PD controller. One call = one control step."""
from config import KP, KD


class LineFollower:
    def __init__(self, drive, sensors):
        self.drive = drive
        self.sensors = sensors
        self.last_error = 0

    def step(self, base_speed):
        """TODO:
        1. error = sensors.error()
        2. if None: lost line -> keep turning toward self.last_error's side
        3. correction = KP*error + KD*(error - last_error)
        4. drive.drive(base + correction, base - correction)  (swap signs if it steers away)
        5. store last_error
        Return True if the line is currently found, False if lost (main uses this for recovery)."""

    def reset(self):
        self.last_error = 0
