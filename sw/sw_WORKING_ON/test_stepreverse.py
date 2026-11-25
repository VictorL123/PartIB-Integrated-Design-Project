from robot import Robot
from utime import ticks_ms, sleep_ms, ticks_diff
from config import BASE_SPEED, SPIN_SPEED

def test_drive():
    robot = Robot()
    t0 = ticks_ms()
    print("reversing")
    while ticks_diff(ticks_ms(), t0) < 10000: 
        robot.follower.stepreverse(BASE_SPEED)
    sleep_ms(1000)
    while robot.sensors.at_junction() == False:
        robot.follower.step(BASE_SPEED) # forward
    print("attempting left halfspin")
    robot.follower.turn("LEFT", SPIN_SPEED, polarity="N") # left halfspin
    while robot.sensors.at_junction() == False:
            robot.follower.step(BASE_SPEED) # forward MANUALLY TURN AROUND
    print("attempting right halfspin")
    robot.follower.turn("RIGHT", SPIN_SPEED, polarity="N") # right halfspin

    robot.drive.stop()
    print("stopped")


if __name__ == "__main__":
    test_drive()

    
    

