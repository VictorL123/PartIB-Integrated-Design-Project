from robot import Robot
from config import BASE_SPEED, SPIN_SPEED, STRAIGHT_BEFORE_TURN
from utime import ticks_ms, ticks_diff, sleep_ms



def running(robot):
    #robot.lights.amber_flash(True)
    print("Running")
    if robot.sensors.at_junction():
        print("At junction")
        robot.follower.turn("RIGHT",SPIN_SPEED)
    robot.follower.step(BASE_SPEED)

        
    
    

def main():    
    robot = Robot()
    #robot.lights.amber_on()
    #print("Amber ON")
    #sleep_ms(500)


    while True:
        running(robot)
    

main()