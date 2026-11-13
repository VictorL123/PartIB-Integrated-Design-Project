"""main.py - the state machine ONLY. Aim: fits on 2 sides of A4 (brief requirement).

Each state does one job and names the next state. No pin numbers, no maths in here.
"""
from utime import ticks_ms, sleep_ms, ticks_diff
from config import *
from robot import Robot
import time


def run():
    robot = Robot()
    state = "WAIT_START"
    t_start = 0

    while True:
        # --- safety first, every loop ---
        # TODO: if stop_pressed(): stop motors, lights off, state = "WAIT_START"
        # TODO: if time is nearly up and state is not RETURN/DONE: plan_to("START"), state = "RETURN"
        # distance sensor safety check here? - change state to recover if state is not already grab or approach package

        if state == "WAIT_START":
            # TODO: wait for start_pressed(); record t_start; amber flash on; plan first trip
            robot.lights.amber_on()
            sleep_ms(2000)
            robot.navigate.plan_to("LINE_FOLLOWER_TEST")
            t_start = ticks_ms()
            state = "TRAVEL"
        elif state == "TRAVEL":
            # TODO: follower.step(); on junction -> route.next_move() -> turn() or wait_for_green()
            #       if line lost too long -> "RECOVER"; if route.arrived() -> next state
            elapsed = ticks_diff(ticks_ms(),t_start)
            robot.lights.amber_flash(elapsed)

            while robot.navigate._arrived() == False:
                if robot.sensors.at_junction():
                    if robot.navigate.peek_next_move() == "STRAIGHT":
                        robot.navigate.next_move()
                        print("calling straight")
                        robot.follower.step(BASE_SPEED)
                        sleep_ms(250)

                    elif robot.navigate.peek_next_move() == "STRAIGHT1S":
                        robot.navigate.next_move()
                        print("calling straight 1 s")
                        t_end = time.time() + STRAIGHT_TIME_BAY
                        while time.time() < t_end:
                            robot.follower.step(BASE_SPEED)
                        robot.follower.turn("180", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "LEFTTURN":
                        print("calling left turn")
                        robot.navigate.next_move()
                        robot.follower.turn("LEFT", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "RIGHTTURN":
                        robot.navigate.next_move()
                        print("calling turn from main")
                        robot.follower.turn("RIGHT", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "ABOUTTURN":
                        robot.navigate.next_move()
                        print("calling about turn")
                        robot.follower.turn("180", SPIN_SPEED)
                        
                    elif robot.navigate.peek_next_move() == "WAIT2S":
                        robot.navigate.next_move()
                        t_end = time.time() + WAIT_TIME
                        print("waiting 2s")
                        while time.time() < t_end:
                            robot.drive.stop()

                    elif robot.navigate.peek_next_move() == "RIGHTTURNINTOBAY":
                        robot.navigate.next_move()
                        print("calling right turn into bay")
                        robot.follower.turn("RIGHT", SPIN_SPEED)
                        t_end = time.time() + STRAIGHT_TIME
                        while time.time() < t_end:
                            print("Going straight after turning into bay")
                            robot.follower.step(BASE_SPEED)
                        t_end = time.time() + WAIT_TIME
                        print("waiting 2s")
                        while time.time() < t_end:
                            robot.drive.stop()
                        robot.follower.turn("180", SPIN_SPEED)
                        
                    elif robot.navigate.peek_next_move() == "LEFTTURNINTOBAY":
                        robot.navigate.next_move()
                        print("calling left turn into bay")
                        t_end = time.time() + STRAIGHT_TIME_DEPOT
                        while time.time() < t_end:
                            robot.follower.step(BASE_SPEED)
                        t_end = time.time() + WAIT_TIME
                        print("waiting 2s")
                        while time.time() < t_end:
                            robot.drive.stop()
                        robot.follower.step(-BASE_SPEED)

                    elif robot.navigate.peek_next_move() == "STOP":
                        robot.navigate.next_move()
                        print("stopping")
                        #specifically just for linefollower
                        robot.drive.stop()
                
                    #if robot.navigate._arrived() == False:
                robot.follower.step(BASE_SPEED)

                if robot.navigate._arrived() == True:
                    if robot.sensors.at_junction():
                        robot.lights.amber_off()
                        robot.drive.stop()


                    
            
        elif state == "APPROACH_PACKAGE":
            # TODO: follow line slowly until package_near(); stop; -> "GRAB"
            pass
        elif state == "GRAB":
            # TODO: close, raise to CARRY, read_polarity(), show_polarity(), plan to N or S depot
            pass
        elif state == "DELIVER":
            # TODO: travel to depot, lower, open, polarity lights off, back off, -> next rack or RETURN
            pass
        elif state == "RECOVER":
            # TODO: stop, search for the line; decide how to give up safely
            pass
        elif state == "RETURN":
            # TODO: travel to START, park inside the box, amber off, -> "DONE"
            pass
        elif state == "DONE":
            pass

        sleep_ms(5)


try:
    run()
finally:
    # Whatever goes wrong, leave the robot safe. TODO: stop motors, actuator, lights.
    pass
