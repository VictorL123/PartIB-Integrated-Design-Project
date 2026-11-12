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
        self.integral = 0

    def step(self, base_speed):
        """TODO:
        1. error = sensors.error()
        2. if None: lost line -> keep turning toward self.last_error's side
        3. correction = KP*error + KD*(error - last_error)
        4. drive.drive(base + correction, base - correction)  (swap signs if it steers away)
        5. store last_error
        Return True if the line is currently found, False if lost (main uses this for recovery)."""
        if self.sensors.at_junction() == False:
            error = self.sensors.error()
            if error == None:
                self.drive.stop()
                return False
            self.integral = error * DT 
            derivative = (error - self.last_error)/DT
            mdelta = KD * derivative + KP * error + KI * self.integral
            self.drive.drive(base_speed + mdelta, base_speed - mdelta)
            self.last_error = error

        return True
    



    def turn(self, spin_speed, direction):
        self.drive.stop()
        #check that there is a line in expected direction of turn
        values = self.sensors.read()
        if (direction == "LEFT" and values == [1,1,1,0]) or (direction == "RIGHT" and values == [0,1,1,1]) or (direction == "180" and values == [0,1,1,0]):
            while self.sensors.centre_on_line() == False:
                self.drive.spin(direction, spin_speed)
                # break if robot about to hit anything
            self.drive.stop()
        else:
            print("line not found")
        
        


    def reset(self):
        self.last_error = 0
