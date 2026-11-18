"""main.py - the state machine ONLY. Aim: fits on 2 sides of A4 (brief requirement).

Each state does one job and names the next state. No pin numbers, no maths in here.
"""
from utime import ticks_ms, sleep_ms, ticks_diff
from config import *
from robot import Robot
from machine import Pin
import time


def run():
    robot = Robot()
    state = "WAIT_START"
    t_start = 0
    reversing = False

    while True:
        # --- safety first, every loop ---
        # TODO: if stop_pressed(): stop motors, lights off, state = "WAIT_START"
        # TODO: if time is nearly up and state is not RETURN/DONE: plan_to("START"), state = "RETURN"
        # distance sensor safety check here? - change state to recover if state is not already grab or approach package

        if state == "WAIT_START":
            robot.lights.amber_off()
            # TODO: wait for start_pressed(); record t_start; amber flash on; plan first trip
            #robot.lights.amber_on()
            sleep_ms(2000)
            robot.navigate.plan_to("LINE_FOLLOWER_TEST")
            #robot.navigate.plan_to("rack_L_low")
            t_start = ticks_ms()
            state = "TRAVEL"
        elif state == "TRAVEL":
            # TODO: follower.step(); on junction -> route.next_move() -> turn() or wait_for_green()
            #       if line lost too long -> "RECOVER"; if route.arrived() -> next state
            elapsed = ticks_diff(ticks_ms(),t_start)
            robot.lights.amber_flash(elapsed)
            robot.lights.red_green_test(elapsed) #Tests the red and green LEDs have been soldered correctly lmao

            if robot.navigate.arrived() == False:
                if robot.sensors.at_junction():
                    reversing = False
                    if robot.navigate.peek_next_move() == "STRAIGHT":
                        robot.navigate.next_move()
                        print("calling straight")
                        robot.follower.step(BASE_SPEED)
                        sleep_ms(250)

                    elif robot.navigate.peek_next_move() == "STRAIGHT1S":
                        robot.navigate.next_move()
                        print("calling straight for straight_time_bay")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < STRAIGHT_TIME_BAY:
                            robot.follower.step(BASE_SPEED)
                        robot.follower.turn("180", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "LEFTTURN":
                        # steps so must be going forward
                        robot.follower.step(BASE_SPEED)
                        print("calling left turn")
                        robot.navigate.next_move()
                        robot.follower.turn("LEFT", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "RIGHTTURN":
                        # steps so must be going forward
                        robot.follower.step(BASE_SPEED)
                        reversing = False
                        print("calling turn from main")
                        robot.navigate.next_move()
                        robot.follower.turn("RIGHT", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "ABOUTTURN":
                        robot.navigate.next_move()
                        print("calling about turn")
                        robot.follower.turn("180", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "RIGHTTURNINTOBAY":
                        robot.navigate.next_move()
                        print("calling right turn into bay")
                        robot.follower.turn("RIGHT", SPIN_SPEED)
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(),t0) < STRAIGHT_TIME_BAY*1000:
                            robot.follower.step(BASE_SPEED)
                        print("stopping")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(),t0) < WAIT_TIME*1000:
                            print("waiting 2s in bay")
                            robot.drive.stop()
                        reversing = True

                        
                    elif robot.navigate.peek_next_move() == "LEFTTURNINTODEPOSIT":
                        robot.navigate.next_move()
                        print("calling left turn into depo")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < STRAIGHT_TIME_DEPOT*1000:
                            robot.follower.step(BASE_SPEED)
                        t0 = ticks_ms()
                        print("waiting 2s in deposit")
                        while ticks_diff(ticks_ms(), t0) < WAIT_TIME*1000:
                            robot.drive.stop()
                        reversing = True
                        #robot.follower.stepreverse(BASE_SPEED) 
                        #sleep_ms(250)
                        
                    elif robot.navigate.peek_next_move() == "REVERSERIGHTTURN":
                        robot.navigate.next_move()
                        print("calling turn from main")
                        robot.follower.turn("RIGHT", SPIN_SPEED, reversing=True)
                        
                    elif robot.navigate.peek_next_move() == "REVERSE":
                        print("reversing!!!")
                        reversing = True
                        robot.follower.reverse(BASE_SPEED) # using reverse not step reverse - unsure
                        sleep_ms(250)
                        robot.navigate.next_move()

                    elif robot.navigate.peek_next_move() == "STOP":
                        robot.navigate.next_move()
                        print("stopping")
                        robot.follower.step(BASE_SPEED)
                        sleep_ms(500)
                        robot.drive.stop()

                if reversing == True:
                    robot.follower.reverse(BASE_SPEED) #using step reverse - haven't seen this work yet?
                else:
                    robot.follower.step(BASE_SPEED)

            if robot.navigate.arrived() == True:
                """when not for the linefollower, this just means that have reached end of route
                TODO: need to load either next route or next state"""
                robot.drive.stop()
                

        elif state == "SEARCH":
            # TODO: go through rack; turn; follow line to make sure pointing in right direction; package_there() -> search next or APPROACH_PACKAGE
            pass  
            
        elif state == "APPROACH_PACKAGE":
            # TODO: follow line slowly until package_near(); stop; read_polarity -> "GRAB"
            pass
        elif state == "GRAB":
            # do we grab before we read_polarity?
            # TODO: close, raise to CARRY, show_polarity(), plan to N or S depot
            pass
        elif state == "DELIVER":
            # TODO: lower, open, polarity lights off, back off, -> next rack or RETURN
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

def main():
    "Check if button pressed"
    stop_button = Pin(START_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN) 
    start = 1
    while start == 1:
        # Poll the value
        start = stop_button.value()
        print(start) 
    run()

main()