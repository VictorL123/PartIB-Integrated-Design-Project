"""main.py - the state machine ONLY. Aim: fits on 2 sides of A4 (brief requirement).

Each state does one job and names the next state. No pin numbers, no maths in here.
"""
from utime import ticks_ms, sleep_ms, ticks_diff
from config import *
from robot import Robot
from machine import Pin
from ir_receiver import wait_for_green
from magnet import read_polarity, read_polarity_grabber_test
from map import table
from buttons import start_pressed, stop_pressed

stop_button = Pin(START_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN) 

def run():
    robot = Robot()
    state = "WAIT_START"
    t_start = 0
    reversing = False
    bay_count = 0
    timeup = False
    no_box_in_rack = False

    while True:
        # --- safety first, every loop ---
        # TODO: if stop_pressed(): stop motors, lights off, state = "WAIT_START"
        
        if stop_pressed(stop_button):
            state = "DONE"
        
        # TODO: if time is nearly up and state is not RETURN/DONE: plan_to("START"), state = "RETURN"

        if ticks_diff(ticks_ms(), t_start) < 10000: # if less than 10s left + not mid deliver, just go home
            timeup = True

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

            if robot.navigate.arrived() == False:
                if robot.sensors.at_junction():
                    reversing = False
                    if robot.navigate.peek_next_move() == "STRAIGHT":
                        robot.navigate.next_move()
                        print("calling straight")
                        robot.follower.step(BASE_SPEED)
                        sleep_ms(250)

                    elif robot.navigate.peek_next_move() == "STRAIGHT_RAMP":
                        #This is trying to eliminate the issue of the line sensors getting too close or far from the ground
                        #on the UP PART OF THE RAMP by forcing it to drive for a set time RAMP_CLOCK_UP
                        robot.navigate.next_move()
                        print("up the ramp we go hehe")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < RAMP_CLOCK_UP:
                            robot.follower.step(RAMP_SPEED)
                        print("ramp complete :)")

                    elif robot.navigate.peek_next_move() == "DOWN_RAMP":
                        #This is a similar move to above, but ajusted for the effects of gravity. It forces drive for a set time
                        robot.navigate.next_move()
                        print("we goin down lol")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < RAMP_CLOCK_DOWN:
                            robot.follower.step(BASE_SPEED)
                        print("back at the bottom now hehe")

                    elif robot.navigate.peek_next_move() == "STRAIGHT1S":
                        robot.navigate.next_move()
                        print("calling straight for straight_time_bay")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < STRAIGHT_TIME_BAY:
                            robot.follower.step(BASE_SPEED)
                        robot.follower.turn("180", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "LEFTTURN":
                        # TODO: check that halfspin works
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

                    elif robot.navigate.peek_next_move() == "WAIT_LIGHTS":
                        # Now we have arrived at the start and want to head up the ramp....
                        robot.navigate.next_move()
                        result = False
                        while result == False:
                            result = wait_for_green()
                        print("lights out and away we go!")

                    elif robot.navigate.peek_next_move() == "LEFTTURNINTOBAY":
                        robot.navigate.next_move()
                        print("calling left turn into bay")
                        robot.follower.turn("LEFT", SPIN_SPEED)
                        
                        #level = robot.navigate.location[-3:]
                        #robot.grabber.raise_before_grab(level)
                        
                        robot.drive.stop()
                        robot.grabber.open()
                        
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(),t0) < STRAIGHT_TIME_BAY:
                            robot.follower.step(BASE_SPEED)
                        print("stopping")

                    elif robot.navigate.peek_next_move() == "RIGHTTURNINTOBAY":
                        robot.navigate.next_move()
                        print("calling right turn into bay")
                        robot.follower.turn("RIGHT", SPIN_SPEED)
                        
                        level = robot.navigate.location[-3:]
                        #robot.grabber.raise_before_grab(level)
                        
                        robot.drive.stop()
                        robot.grabber.open()
                        
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(),t0) < STRAIGHT_TIME_BAY:
                            robot.follower.step(BASE_SPEED)
                        print("stopping")
                        
                        # TODO: REMOVE THIS CODE AFTER GRABBER TEST
                        bay_count = 1
                        robot.navigate.location = "rack_L_low"
                        robot.drive.stop()
                        state = "GRAB"
                        
                        # print("SHOULD NOT BE PRINTING THIS FROM TRAVEL")
                        
                        # t0 = ticks_ms()
                        # while ticks_diff(ticks_ms(),t0) < WAIT_TIME:
                        #     #print("waiting 2s in bay")
                        #     robot.drive.stop()
                        # reversing = True

                    # TODO: This is again just for the grabber test    
                    elif robot.navigate.peek_next_move() == "LEFTTURNINTODEPOSIT":
                        robot.navigate.next_move()
                        state = "DELIVER"

                        
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
                        state = "DONE"

                if reversing == True:
                    robot.follower.reverse(BASE_SPEED) # not using step reverse - haven't seen this work yet?
                else:
                    robot.follower.step(BASE_SPEED)

            if robot.navigate.arrived() == True:
                """when not for the linefollower, this just means that have reached end of route
                TODO: need to load either next route or next state"""
                robot.drive.stop()

                if timeup:
                    state = "RETURN"

                # decide on next state by location
                elif robot.navigate.location in ("rack_L_low", "rack_R_low", "rack_L_top", "rack_R_top"):
                    state = "SEARCH"

                elif robot.navigate.location in ("deposit_L1", "deposit_L2", "deposit_R1", "deposit_R2"):
                    state = "DELIVER"

                elif robot.navigate.location == "START":
                    if robot.navigate.nextlocation != "None": # need to check if there's not more to do:
                        robot.navigate.plan_to(robot.navigate.nextlocation)
                        robot.navigate.nextlocation = "None"
                        state = "TRAVEL"
                    else: 
                        state = "DONE"


        elif state == "SEARCH": 
            # set up symmetric directions
            if robot.navigate.location in ("rack_L_low", "rack_R_top"):
                turnin = "RIGHT"
                turnout = "LEFT"
            elif robot.navigate.location in ("rack_R_low", "rack_L_top"):
                turnin = "LEFT"
                turnout = "RIGHT"
            # now can use same code for both sides
            if robot.sensors.at_junction():
                bay_count += 1
                print(bay_count)
                robot.follower.turn(turnin, SPIN_SPEED)
                print(f"calling {turnin} turn")
                t0 = ticks_ms()
                while ticks_diff(ticks_ms(), t0) < STRAIGHT_TIME_SEARCH:
                    robot.follower.step(BASE_SPEED)
                robot.drive.stop()
                if robot.distance.package_there():
                    print("package there")
                    no_box_in_rack = False
                    state = "APPROACH_PACKAGE"
                else:
                    print("package not there")
                    while robot.sensors.at_junction == False:
                        robot.follower.reverse(BASE_SPEED)
                    if timeup:
                        state = "RETURN"
                    if bay_count < 6:
                        #keep going to search next bay
                        robot.follower.turn(turnout, SPIN_SPEED)
                    else: 
                        #give up, go to next rack. raise error
                        print("Error: no magnet found in rack")
                        robot.follower.turn(turnin, SPIN_SPEED)
                        
                        no_box_in_rack = True
                        state = "TOFIRSTBAY"                                

                robot.follower.step(BASE_SPEED)
                  
            
        elif state == "APPROACH_PACKAGE":
            elapsed = ticks_diff(ticks_ms(),t_start)
            robot.lights.amber_flash(elapsed)
            
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
                    no_box_in_rack = False
                    state = "GRAB"
                    
                # If box has no polarity then search next bay
                elif polarity == None:
                    t0 = ticks_ms()
                    while ticks_diff(ticks_ms(), t0) < FORWARD_BEFORE_GRAB:
                        robot.follower.reverse(EXTRA_SLOW_SPEED)
                    while robot.sensors.at_junction() == False:
                        robot.follower.reverse(BASE_SPEED)

                    # Turn back into straight
                    robot.follower.step(BASE_SPEED)
                    if robot.navigate.location in ("rack_L_low", "rack_R_top"):
                        robot.follower.turn("LEFT", SPIN_SPEED, reversing=True)
                    elif robot.navigate.location in ("rack_R_low", "rack_L_top"):
                        robot.follower.turn("RIGHT", SPIN_SPEED, reversing=True)
                    
                    state = "SEARCH"

                
        elif state == "GRAB": 

            print("In state Grabbing")

            # recording this rack as searched
            table[robot.navigate.location] = "SEARCHED"
            
            robot.drive.stop()
            sleep_ms(300)
            robot.grabber.close()
            sleep_ms(300)
            robot.grabber.pick_up()
            
            # May not need to read again because we read in approach package
            polarity = read_polarity_grabber_test()
            robot.lights.show_polarity(polarity)
            
            sleep_ms(300)
            
            while ticks_diff(ticks_ms(), t0) < FORWARD_BEFORE_GRAB:
                robot.follower.reverse(EXTRA_SLOW_SPEED)
            
            while robot.sensors.at_junction() == False:
                robot.follower.reverse(BASE_SPEED)
            
            # Turn back into straight
            if robot.navigate.location == "rack_L_low":
                print("Turning right after bay")
                robot.follower.step(BASE_SPEED)
                robot.follower.turn("RIGHT", SPIN_SPEED, reversing=True)

            elif robot.navigate.location in ("rack_R_low", "rack_L_top"):
                print("Turning left after bay")
                robot.follower.step(BASE_SPEED)
                robot.follower.turn("LEFT", SPIN_SPEED, reversing=True)
                
            # Get to the first bay
            state = "TOFIRSTBAY"
            
        elif state == "TOFIRSTBAY":
            """This gets back to the first bay"""
            print("In state TOFIRSTBAY")
            elapsed = ticks_diff(ticks_ms(),t_start)
            robot.lights.amber_flash(elapsed)
            
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

                    if timeup:
                        state = "RETURN"
                    
                    if no_box_in_rack == True:
                        #need to load route for next rack
                        for i in range(5, 9):
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
                                table["cycles"] += 1
                                robot.navigate.plan_to("rack_L_top")
                            
                            planned = False   

                    # else: 
                        # TODO: plan to take box to right deposit
                                         
                    
                    state = "TRAVEL"
            else:
                robot.follower.step(BASE_SPEED)
                    
            
        elif state == "DELIVER":
            # TODO: lower, open, polarity lights off, back off, -> next rack or RETURN
            elapsed = ticks_diff(ticks_ms(),t_start)
            robot.lights.amber_flash(elapsed)

            # record deposit as full
            table[robot.navigate.location] = "FULL"
            
            while robot.sensors.at_junction() == False:
                robot.follower.step(BASE_SPEED) 
                
            robot.drive.stop()
            sleep_ms(300)    
            
            #deposit box
            robot.grabber.lower_to_ground()
            sleep_ms(400)
            robot.grabber.open()
            sleep_ms(400)
            
            # Turn off polarity lights
            robot.lights.red_off()
            robot.lights.green_off()
            
            t0 = ticks_ms()
            # Get out of depot
            while ticks_diff(ticks_ms(), t0) < BACK_AFTER_DELIVER:
                print("reversing out of depot")
                robot.follower.reverse(EXTRA_SLOW_SPEED) 
            while robot.sensors.at_junction() == False:
                robot.follower.reverse(BASE_SPEED)

            # # Hard code journey home just for grabber test
            # robot.follower.step(BASE_SPEED)
            # robot.follower.turn("RIGHT", SPIN_SPEED, reversing=True)
            # grab_test = True
            if timeup:
                state = "RETURN"
            # if grab_test == True:
            #     state = "TRAVEL"
            else:
                print("SHOULD NOT BE PRINTING THIS")
                #need to load route for next rack
                for i in range(5, 9):
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
                    table["cycles"] += 1
                    robot.navigate.plan_to("rack_L_top")
            
                planned = False
            state = "TRAVEL"
            
        
        elif state == "RECOVER":
            # TODO: stop, search for the line; decide how to give up safely
            pass
        
        elif state == "RETURN":
            # TODO: travel to START, park inside the box, amber off, -> "DONE"
            print("RETURNING HOME")
        
            if bay_count > 0:
                elapsed = ticks_diff(ticks_ms(),t_start)
                robot.lights.amber_flash(elapsed)
                
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

            robot.navigate.plan_to("START")

        elif state == "DONE":
            print("State is DONE")
            robot.drive.stop()
            robot.lights.amber_off()
            robot.lights.red_off()
            robot.lights.green_off()
            #robot.grabber.lower_to_ground()
            robot.grabber.close()
            

        sleep_ms(5)
        t0 = ticks_ms()
        # finetune: only if 2 boxes are delivered, 
        # when 15s left
        # if ticks_diff(t_start, t0) > 255000:
        #     state == "RETURN"


def main():
    """Check if button pressed"""
    if start_pressed(stop_button):
        print("Starting")
        run()

main()