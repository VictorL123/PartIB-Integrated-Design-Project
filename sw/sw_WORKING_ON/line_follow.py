"""line_follow.py - the PD controller. One call = one control step."""
from config import KP, KD, KI, DT, TURN_90_MS, SPIN_SPEED, STRAIGHT_BEFORE_TURN, TURN_180_MS
from utime import sleep_ms

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
    



    def turn(self, direction, spin_speed=SPIN_SPEED):
        print("in turn function")
        if direction in ("LEFT", "RIGHT"):
            duration = TURN_90_MS
            print("before going straight")
            sleep_ms(STRAIGHT_BEFORE_TURN)
            print("after going straight")
            
        elif direction == "180":
            duration = TURN_180_MS
            direction = "RIGHT"          # a U-turn still needs a side to spin toward
        else:
            return
        print("turning")
        self.drive.spin(direction, spin_speed)
        sleep_ms(duration)
        self.drive.stop()                # without this the robot never stops turning
        
        


    def reset(self):
        self.last_error = 0
