"""line_follow.py - the PD controller. One call = one control step."""
from config import KP, KD, KI, DT
from utime import sleep

# what is a control step? where does the line counting happen? what is drive? can drivetrain accommodate changing one wheel?

class LineFollower:
    def __init__(self, robot, sensors):
        # initialise
        self.drive = robot
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
        while self.sensors.at_junction() == False:
            error = self.sensors.error()
            if error == None:
                self.drive.stop()
                return False
            integral = error * DT 
            derivative = (error - self.last_error)/DT
            mdelta = KD * derivative + KP * error + KI * integral
            self.drive.drive(base_speed + mdelta, base_speed - mdelta)
            self.last_error = error

        return True
    



    def spin(self, spin_speed, direction):
        while self.sensors.centre_on_line() == False:
            self.drive.spin(direction, spin_speed)
            # break if robot about to hit anything
        self.drive.stop()
        
        


    def reset(self):
        self.last_error = 0
