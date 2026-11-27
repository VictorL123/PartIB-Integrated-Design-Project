"""line_follow.py - the PD controller. One call = one control step."""
from config import KP, KD, KI, DT, TURN_LEFT_90_MS, TURN_RIGHT_90_MS, SPIN_SPEED, BASE_SPEED, STRAIGHT_BEFORE_TURN, STRAIGHT_BEFORE_HALFSPIN, TURN_180_MS, HALF_TURN_LEFT_TIME
from utime import sleep_ms
# from magnet import read_polarity # for testing, just input polarity
# what is a control step? where does the line counting happen? what is drive? can drivetrain accommodate changing one wheel?

class LineFollower:
    def __init__(self, robot, sensors):
        # initialise
        self.drive = robot
        self.sensors = sensors
        self.last_error = 0
        self.integral = 0

    def step(self, base_speed):
        """ gets error, appplies one instance of PID control. 
        Returns True if the line is currently found, False if lost (use this for recovery?)."""
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

    def stepreverse(self, base_speed):
        # """step as above but in reverse"""
        # error = self.sensors.error()
        # if error == None:
        #     self.drive.stop()
        #     return False
        # self.integral = error * DT 
        # derivative = (error - self.last_error)/DT
        # mdelta = KD * derivative + KP * error + KI * self.integral
        # # TODO: check this works? would then be worth using
        # self.drive.drive(-(base_speed + mdelta), -(base_speed - mdelta))
        # self.last_error = error
        print("don't call this nonsense again!")
        return True

    def reverse(self, base_speed):
        """reverse with no PID control"""
        self.drive.drive(-base_speed, -base_speed)


    def turn(self, direction, spin_speed=SPIN_SPEED, polarity=None, reversing=False):
        """turn left, right or 180 TODO: needs a bit of tidying"""
        print("In turn function")
        if direction == "LEFT":
            duration = TURN_LEFT_90_MS
            print("before going straight")
            
        elif direction == "RIGHT":
            duration = TURN_RIGHT_90_MS
            print("before going straight")
            
        elif direction == "180":
            duration = TURN_180_MS
            direction = "RIGHT"          # a U-turn still needs a side to spin toward
        else:
            print("BROKEN")
            return
        
        # if read_polarity() == None:
        if polarity == None:
            if direction != "180" and reversing == False:
                # self.drive(BASE_SPEED, BASE_SPEED)
                sleep_ms(STRAIGHT_BEFORE_TURN)
                print("after going straight")
            elif direction != "180" and reversing == True:
                # self.drive(BASE_SPEED, BASE_SPEED)
                sleep_ms(STRAIGHT_BEFORE_TURN+50)            # TODO: needs calibrating - value is equivalent of thickness of the line
                print("after going straight")
            print("turning")
            self.drive.spin(direction, spin_speed)
            sleep_ms(duration)
            self.drive.stop()                # without this the robot never stops turning
        else:
            if direction != "180":
                sleep_ms(STRAIGHT_BEFORE_HALFSPIN) # 0 s straight before turn for now # TODO: calibrate
            print("turning halfspin")
            self.drive.halfspin(direction, spin_speed)
            sleep_ms(HALF_TURN_LEFT_TIME)
            self.drive.stop() 


    def reset(self):
        self.last_error = 0
