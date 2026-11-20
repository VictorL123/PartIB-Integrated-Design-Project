"""main.py - the state machine ONLY. Aim: fits on 2 sides of A4 (brief requirement).

Each state does one job and names the next state. No pin numbers, no maths in here.
"""
from utime import ticks_ms, sleep_ms, ticks_diff
from config import *
from robot import Robot
from distance import DistanceSensor
from machine import Pin
from magnet import read_polarity
from lights import Lights
from ir_receiver import wait_for_green
import time
from map import table


def run():
    robot = Robot()
    state = "WAIT_START"
    t_start = 0
    reversing = False
    bay_count = 0

    while True:
        # --- safety first, every loop ---
        # TODO: if stop_pressed(): stop motors, lights off, state = "WAIT_START"
        # TODO: if time is nearly up and state is not RETURN/DONE: plan_to("START"), state = "RETURN"
        # distance sensor safety check here? - change state to recover if state is not already grab or approach package

        if state == "WAIT_START":
            robot.lights.amber_off()
            robot.lights.red_off()
            robot.lights.green_off() #Turn all the lights off at the start
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
                        while ticks_diff(ticks_ms(),t0) < STRAIGHT_TIME_BAY:
                            robot.follower.step(BASE_SPEED)
                        print("stopping")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(),t0) < WAIT_TIME:
                            print("waiting 2s in bay")
                            robot.drive.stop()
                        reversing = True

                        
                    elif robot.navigate.peek_next_move() == "LEFTTURNINTODEPOSIT":
                        robot.navigate.next_move()
                        print("calling left turn into depo")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < STRAIGHT_TIME_DEPOT:
                            robot.follower.step(BASE_SPEED)
                        t0 = ticks_ms()
                        print("waiting 2s in deposit")
                        while ticks_diff(ticks_ms(), t0) < WAIT_TIME:
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
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < 200:
                            robot.follower.step(BASE_SPEED)
                        robot.drive.stop()

                if reversing == True:
                    robot.follower.reverse(BASE_SPEED) #using step reverse - haven't seen this work yet?
                else:
                    robot.follower.step(BASE_SPEED)

            if robot.navigate.arrived() == True:
                """when not for the linefollower, this just means that have reached end of route
                TODO: need to load either next route or next state"""
                robot.drive.stop()
                #decide on next state by location
                if robot.navigate.location in ("rack_L_low", "rack_R_low", "rack_L_top", "rack_R_top"):
                    state = "SEARCH"
                elif robot.navigate.location in ("deposit_L1", "deposit_L2", "deposit_R1", "deposit_R2"):
                    state = "DELIVER"

        elif state == "SEARCH":
            # TODO: go through rack; turn; follow line to make sure pointing in right direction; package_there() -> search next or APPROACH_PACKAGE
            if robot.navigate.location in ("rack_L_low", "rack_L_top"):
                if robot.sensors.at_junction():
                    bay_count += 1
                    print(bay_count)
                    robot.follower.turn("RIGHT", SPIN_SPEED)
                    print("calling right turn")
                    t0 = ticks_ms()
                    while ticks_diff(ticks_ms(), t0) < STRAIGHT_TIME_SEARCH:
                        robot.follower.step(BASE_SPEED)
                    robot.drive.stop()
                    if robot.distance.package_there():
                        print("package there")
                        state = "APPROACH_PACKAGE"
                    else:
                        print("package not there")
                        while robot.sensors.at_junction == False:
                            robot.follower.reverse(BASE_SPEED)
                        if bay_count < 6:
                            #keep going to search next bay
                            robot.follower.turn("LEFT", SPIN_SPEED)
                        else: 
                            #give up, go to next rack. raise error
                            print("Error: no magnet found in rack")
                            robot.follower.turn("RIGHT", SPIN_SPEED)
                            
                            no_box_in_rack = True
                            state = "TOFIRSTBAY"                                

                robot.follower.step(BASE_SPEED)
                  
            
        elif state == "APPROACH_PACKAGE":
            # TODO: follow line slowly until package_near(); stop; read_polarity -> "GRAB"
            if robot.distance.package_near() != True:
                robot.follower.step(SLOW_SPEED)
                
            elif robot.distance.package_near():
                # Drive forward for a given amount
                t0 = ticks_ms()
                while ticks_diff(ticks_ms(), t0) < FORWARD_BEFORE_GRAB:
                    robot.follower.step(EXTRA_SLOW_SPEED)
                robot.drive.stop()
                
                # Check polarity of box
                polarity = read_polarity()
                
                # If polarity is either "N" or "S"
                if polarity != None:
                    state = "GRAB"
                    
                # If box has no polarity then search next bay
                elif polarity == None:
                    t0 = ticks_ms()
                    while ticks_diff(ticks_ms(), t0) < FORWARD_BEFORE_GRAB:
                        robot.follower.reverse(EXTRA_SLOW_SPEED)
                    while robot.sensors.at_junction() == False:
                        robot.follower.reverse(BASE_SPEED)
                        
                    # Turn back into straight
                    if robot.navigate.location == "rack_L_low":
                        robot.follower.turn("LEFT", SPIN_SPEED)
                    elif robot.navigate.location == "rack_R_low":
                        robot.follower.turn("RIGHT", SPIN_SPEED)
                    elif robot.navigate.location == "rack_L_top":
                        robot.follower.turn("RIGHT", SPIN_SPEED)
                    elif robot.navigate.location == "rack_R_top":
                        robot.follower.turn("LEFT", SPIN_SPEED)
                    state = "SEARCH"

                
        elif state == "GRAB":
            # TODO: 
            # (haven't coded anything for what the closest depo is)

            # need to assign current rack as "SEARCHED" -> still not sure of the best way to save these values
            
            robot.grabber.close()
            level = robot.navigate.location[-3:]
            robot.grabber.raise_to(level)
            
            # May not need to read again because we read in approach package
            polarity = read_polarity()
            robot.lights.show_polarity(polarity)
            
            while ticks_diff(ticks_ms(), t0) < FORWARD_BEFORE_GRAB:
                robot.follower.reverse(EXTRA_SLOW_SPEED)
            
            while robot.sensors.at_junction() == False:
                robot.follower.reverse(BASE_SPEED)
            
            # Turn back into straight
            if robot.navigate.location == "rack_L_low":
                robot.follower.turn("RIGHT", SPIN_SPEED)
            elif robot.navigate.location == "rack_R_low":
                robot.follower.turn("LEFT", SPIN_SPEED)
            elif robot.navigate.location == "rack_L_top":
                robot.follower.turn("LEFT", SPIN_SPEED)
            elif robot.navigate.location == "rack_R_top":
                robot.follower.turn("RIGHT", SPIN_SPEED)
                
            # Get to the first bay
            state = "TOFIRSTBAY"
            
        elif state == "TOFIRSTBAY":
            """This gets to the first bay"""
            if robot.sensors.at_junction():
                if bay_count > 1:
                    bay_count -= 1
                    print("calling straight")
                    robot.follower.step(BASE_SPEED)
                    sleep_ms(250)
                else:
                    # reached last bay
                    print("end of rack")
                    bay_count -= 1
                    
                    if no_box_in_rack == True:
                        #need to load route for next rack
                        for i in range(4, 8):
                            # cycle through the first dictionary entries for racks
                            # not looking at where is next closest!!
                            val = list(table.values())[i]
                            if val == "UNSEARCHED":
                                robot.navigate.plan_to(list(table)[i])
                                planned = True
                                break

                            # if here then all racks are recorded as searched
                            if planned == False:
                                # have to use planned variable as some routes (eg from top left rack to top right) are empty
                                print("error, all racks searched")
                                table["rack_L_low"], table["rack_L_top"], table["rack_R_low"], table["rack_R_top"] = "UNSEARCHED"
                                robot.navigate.plan_to("rack_L_top")
                            
                            planned = False                        
                    
                    state = "TRAVEL"
            else:
                robot.follower.step(BASE_SPEED)
                    
            
        elif state == "DELIVER":
            # TODO: lower, open, polarity lights off, back off, -> next rack or RETURN
            t0 = ticks_ms()
            while robot.sensors.at_junction() == False:
                robot.follower.step(BASE_SPEED)
            while ticks_diff(ticks_ms(), t0) < FORWARD_BEFORE_DELIVER:
                robot.follower.step(EXTRA_SLOW_SPEED) 
                
            #deposit box
            robot.grabber.lower_to_ground()
            robot.grabber.open()
            
            # Turn off polarity lights
            robot.lights.red_off()
            robot.lights.green_off()
            
            # Get out of depot
            while ticks_diff(ticks_ms(), t0) < BACK_AFTER_DELIVER:
                robot.follower.reverse(EXTRA_SLOW_SPEED) 
            while robot.sensors.at_junction() == False:
                robot.follower.reverse(BASE_SPEED)

            #need to load route for next rack
            for i in range(4, 8):
                # cycle through the first dictionary entries for racks
                # not looking at where is next closest!!
                val = list(table.values())[i]
                if val == "UNSEARCHED":
                    robot.navigate.plan_to(list(table)[i])
                    planned = True
                    break

            # if here then all racks are recorded as searched
            if planned == False:
                # have to use planned variable as some routes (eg from top left rack to top right) are empty
                print("error, all racks searched")
                table["rack_L_low"], table["rack_L_top"], table["rack_R_low"], table["rack_R_top"] = "UNSEARCHED"
                robot.navigate.plan_to("rack_L_top")
        
            planned = False
            state = "TRAVEL"
            
        
        elif state == "RECOVER":
            # TODO: stop, search for the line; decide how to give up safely
            pass
        
        elif state == "RETURN":
            # TODO: travel to START, park inside the box, amber off, -> "DONE"
            pass

        elif state == "DONE":
            pass

        sleep_ms(5)
        t0 = ticks_ms()
        # finetune: only if 2 boxes are delivered, 
        # when 15s left
        # if ticks_diff(t_start, t0) > 255000:
        #     state == "RETURN"


def main():
    """Check if button pressed"""
    stop_button = Pin(START_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN) 
    start = 1
    wait_for_green()
    while start == 1:
        # Poll the value
        start = stop_button.value()
    print("Starting")
    run()

main()