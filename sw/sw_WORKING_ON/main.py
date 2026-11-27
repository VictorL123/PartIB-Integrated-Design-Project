"""main.py - the state machine ONLY. Aim: fits on 2 sides of A4 (brief requirement).

Each state does one job and names the next state. No pin numbers, no maths in here.
"""
from utime import ticks_ms, sleep_ms, ticks_diff
from config import *
from robot import Robot
from machine import Pin
from ir_receiver import wait_for_green
from magnet import read_polarity, read_polarity_fake
from map import table
from buttons import start_pressed, stop_pressed

stop_button = Pin(START_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN) 

def run():
    robot = Robot()
    state = "WAIT_START"
    t_start = ticks_ms()
    reversing = False # used in linefollow turn to check if it needs to clear the junction before turning or not (if just reversed on, -thickness for forward movement)
    bay_count = 0
    timeup, time_deliver_up = False, False

    # no_box_in_rack = False # USING CHECK POLARITY INSTEAD?

    while True:
        #Check 
        if stop_pressed(stop_button):
            state = "DONE"

        # TODO: Check time to go home
        # If its been 4:35 since start, go home
        if ticks_diff(ticks_ms(), t_start) > 275000: # if less than 25s left + not mid deliver, just go home
            # currently, this is only checked after making one TRAVEL, after making one SEARCH , after getting to the end of a bay and after delivering
            timeup = True
        if ticks_diff(ticks_ms(), t_start) > 255000: # if less than 45s left before delivering, try to put in closest depo, or just go home
            # this checks after getting to end of first bay before delivering
            time_deliver_up = True

        # distance sensor safety check here? - change state to recover if state is not already grab or approach package

        if state == "WAIT_START":
            """ set all the lights off, choose a navigation scheme, and finally record start time before travel begins """
            
            # Ensure all the lights are off at the start
            robot.lights.amber_off()
            robot.lights.red_off()
            robot.lights.green_off() 
            sleep_ms(1000)
            
            # Set the route to Left rack low
            robot.navigate.plan_to("rack_L_low")
            t_start = ticks_ms()
            state = "TRAVEL"

        elif state == "TRAVEL":
            """ this is the main state, in which the robot is trying to move from one place to the next by following a route specified in navigation """
            elapsed = ticks_diff(ticks_ms(),t_start)
            robot.lights.amber_flash(elapsed)
            
            if robot.sensors.at_junction(): 
                
                
                if robot.navigate.arrived() == False:
                    print("junction......")
                    reversing = False
                    
                    print(robot.navigate.peek_next_move())

                    #Now we look at the next move and execute it in one of the elif ladder below
                    if robot.navigate.peek_next_move() == "STRAIGHT":
                        #If next job is goign forward then begin going forward for at least 250 ms or until junction
                        robot.navigate.next_move()
                        print("calling straight")
                        robot.follower.step(BASE_SPEED)
                        sleep_ms(400)

                    elif robot.navigate.peek_next_move() == "STRAIGHT_RAMP":
                        # This is trying to eliminate the issue of the line sensors getting too close or far from the ground
                        # on the UP PART OF THE RAMP by forcing it to drive for a set time RAMP_CLOCK_UP
                        # TODO: beware of long while loops... no lights
                        robot.navigate.next_move()
                        print("up the ramp we go hehe")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < RAMP_CLOCK_UP:
                            #Flash LEDs on while in the loop
                            robot.lights.amber_flash(ticks_ms())
                            robot.follower.step(RAMP_SPEED)
                        print("ramp complete :)")

                    elif robot.navigate.peek_next_move() == "DOWN_RAMP":
                        #This is a similar move to above, but adjusted for the effects of gravity. It forces drive for a set time
                        robot.navigate.next_move()
                        print("we goin down lol")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < RAMP_CLOCK_DOWN:
                            #Flash LEDs on while in the loop
                            robot.lights.amber_flash(ticks_ms())
                            robot.follower.step(BASE_SPEED)
                        print("back at the bottom now hehe")

                    elif robot.navigate.peek_next_move() == "STRAIGHT1S":
                        #This gets the robot from the bay junction to position to begin executing a grab
                        robot.navigate.next_move()
                        print("calling straight for straight_time_bay")
                        t0 = ticks_ms()
                        while ticks_diff(ticks_ms(), t0) < STRAIGHT_TIME_BAY:
                            #Flash LEDs on while in the loop
                            robot.lights.amber_flash(ticks_ms())
                            robot.follower.step(BASE_SPEED)
                        robot.follower.turn("180", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "LEFTTURN":
                        #Turn forward to the left 90 degrees; steps so must be going forward
                        robot.follower.step(BASE_SPEED)
                        print("calling left turn")
                        robot.navigate.next_move()
                        robot.follower.turn("LEFT", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "RIGHTTURN":
                        #Turn forward to the right 90 degrees; steps so must be going forward
                        robot.follower.step(BASE_SPEED)
                        reversing = False
                        print("calling turn from main")
                        robot.navigate.next_move()
                        robot.follower.turn("RIGHT", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "ABOUTTURN":
                        #Turn the robot fully around, sleeping it so it doesnt detect any white lines it passes over as it turns
                        robot.navigate.next_move()
                        print("calling about turn")
                        robot.follower.turn("180", SPIN_SPEED)

                    elif robot.navigate.peek_next_move() == "WAIT_LIGHTS":
                        # Now we have arrived at the start and want to head up the ramp....
                        robot.navigate.next_move()
                        result = False
                        while result == False:
                            #Flash LEDs on while in the loop
                            robot.lights.amber_flash(ticks_ms())
                            result = wait_for_green()
                        print("lights out and away we go!")
                       
                    elif robot.navigate.peek_next_move() == "REVERSERIGHTTURN":
                        robot.navigate.next_move()
                        print("calling turn from main")
                        robot.follower.turn("RIGHT", SPIN_SPEED, reversing=True)

                    elif robot.navigate.peek_next_move() == "REVERSELEFTTURN":
                        robot.navigate.next_move()
                        print("calling turn from main")
                        robot.follower.turn("LEFT", SPIN_SPEED, reversing=True)
                        
                    elif robot.navigate.peek_next_move() == "REVERSE":
                        print("reversing!!!")
                        reversing = True
                        robot.follower.reverse(BASE_SPEED) # using stepreverse not reverse - unsure
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


                elif robot.navigate.arrived() == True:
                    """when not for the linefollower, this just means that have reached end of route"""
                    robot.drive.stop()

                    if timeup:
                        print("state = RETURN")
                        state = "RETURN"

                    # decide on next state by location
                    elif robot.navigate.location in ("rack_L_low", "rack_R_low", "rack_L_top", "rack_R_top"):
                        print("state = SEARCH")
                        state = "SEARCH"

                    elif robot.navigate.location in ("deposit_L1", "deposit_L2", "deposit_R1", "deposit_R2"):
                        print("state = DELIVER")
                        state = "DELIVER"

                    elif robot.navigate.location == "START":
                        if robot.navigate.nextlocation != "None": # need to check if there's not more to do:
                            print(f"routing to {robot.navigate.nextlocation}")
                            robot.navigate.plan_to(robot.navigate.nextlocation)
                            robot.navigate.nextlocation = "None"
                            state = "TRAVEL"
                        else: 
                            print("done")
                            state = "DONE"

            if reversing == True:
                robot.follower.reverse(BASE_SPEED) # not using step reverse - haven't seen this work yet?
            else:
                robot.follower.step(BASE_SPEED)

        elif state == "SEARCH": 
            
            # set up symmetric directions
            if robot.navigate.location in ("rack_L_low", "rack_R_top"):
                turnin = "RIGHT"
                turnout = "LEFT"
            elif robot.navigate.location in ("rack_R_low", "rack_L_top"):
                turnin = "LEFT"
                turnout = "RIGHT"
                
            # It was doing random reverses so i dont think this bit works - not sure tho?    
                
            # if bay_count > 0:
            #     if robot.sensors.at_junction() != True:
            #         robot.follower.stepreverse(BASE_SPEED)
            #     sleep_ms(250)
                    
            # same code for both sides
            if robot.sensors.at_junction():
                # TODO: (check that) this is assuming each time AGV turns, it ends up on the next junction (if it ends up beyond, that's an issue)
                bay_count += 1
                print(f"at bay {bay_count}")
                print(bay_count)
                
                # Turn into first bay
                robot.follower.turn(turnin, SPIN_SPEED)
                print(f"calling {turnin} turn")
                
                # Raise grabber to correct level
                robot.drive.stop()
                level = robot.navigate.location[-3:]
                robot.grabber.raise_before_grab(level)
                robot.grabber.open()
                
                # Drive until should detect package
                t0 = ticks_ms()
                while ticks_diff(ticks_ms(), t0) < STRAIGHT_TIME_SEARCH:
                    robot.follower.step(BASE_SPEED)
                robot.drive.stop()
                
                if robot.distance.package_there():
                    print("package there")
                    state = "APPROACH_PACKAGE"
                else:
                    print("package not there")
                    
                    # Reverse until at the line
                    while robot.sensors.at_junction() == False:
                        robot.follower.reverse(BASE_SPEED)
                    print("Reverse finished")
                    if timeup:
                        print("state = RETURN")
                        state = "RETURN"
                    if bay_count < 6:
                        # keep going to search next bay
                        print("Turning into next bay")
                        # robot.follower.step(BASE_SPEED)
                        robot.follower.turn(turnout, SPIN_SPEED)
                    else: 
                        # give up, go to next rack. raise error
                        print("Error: no magnet found in rack, back to first bay")
                        robot.follower.turn(turnin, SPIN_SPEED)
                        state = "TOFIRSTBAY"                                

                robot.follower.step(BASE_SPEED)                
            
        elif state == "APPROACH_PACKAGE":
            elapsed = ticks_diff(ticks_ms(),t_start)
            robot.lights.amber_flash(elapsed)
            
            # if robot.distance.package_near() != True:
            #     robot.follower.step(SLOW_SPEED)
                
            # elif robot.distance.package_near():
            #     # Drive forward for a given amount
            #     print("Driving towards package")
            #     t0 = ticks_ms()
            while robot.sensors.off_line() == False:
                robot.follower.step(EXTRA_SLOW_SPEED)
            robot.drive.stop()
            
            # Check polarity of box
            polarity = read_polarity()
            
            # If polarity is either "N" or "S"
            if polarity != None:
                print("state = GRAB")
                state = "GRAB"
                
            # If box has no polarity then search next bay
            elif polarity == None:
                t0 = ticks_ms()
                print("Polarity is nothing")
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

                print("back to state = SEARCH")
                state = "SEARCH"
           
        elif state == "GRAB": 
            # recording this rack as searched
            table[robot.navigate.location] = "SEARCHED"
            
            robot.drive.stop()
            #robot.grabber.pick_up()
            sleep_ms(300)
            robot.grabber.close()
            sleep_ms(300)
            robot.grabber.pick_up()
            sleep_ms(300)
            
            # May not need to read again because we read in approach package
            polarity = read_polarity()
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
            print("state = TOFIRSTBAY")
            state = "TOFIRSTBAY"
            
        elif state == "TOFIRSTBAY":
            """This gets back to the first bay"""
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
                        print("state = RETURN")
                        state = "RETURN"
                    
                    if polarity == None: # if not holding box
                        #need to load route for next rack
                        for i in range(5, 9):
                            # cycle through the first dictionary entries for racks
                            # not looking at where is next closest!!
                            val = list(table.values())[i]
                            if val == "UNSEARCHED":
                                robot.navigate.plan_to(list(table)[i])
                                print(f"planning route to {list(table)[i]}")
                                planned = True # to signal a rack has been chosen and routed to
                                break

                            # if here then all racks are recorded as searched
                            if planned == False:
                                # have to use planned variable as some routes (eg from top left rack to top right) are empty
                                print("error, all racks searched")
                                table["rack_L_low"], table["rack_L_top"], table["rack_R_low"], table["rack_R_top"] = "UNSEARCHED"
                                table["cycles"] += 1
                                robot.navigate.plan_to("rack_L_top")
                            
                            planned = False # to reset

                    else: # so it is carrying a box
                        # assuming there will only be 2 boxes of the same polarity on the table at any time
                        if polarity == "N":
                            if robot.navigate.location != "rack_L_low" and time_deliver_up: # giving it 45s to deliver and get back
                                if robot.navigate.location == "rack_R_low": # just worth putting in wrong box, and getting back to home
                                    if table["deposit_R2"] == "EMPTY":
                                        print("maximise points: planning to deposit_R2")
                                        robot.navigate.plan_to("deposit_R2")
                                    elif table["deposit_R1"] == "EMPTY":
                                        print("planning to deposit_R1")
                                        robot.navigate.plan_to("deposit_R1")
                                else:
                                    state = "RETURN" # only if no closest good depot

                            else: # enough time left to do properly
                                if table["deposit_L2"] == "EMPTY":
                                    print("planning to deposit_L2")
                                    robot.navigate.plan_to("deposit_L2")
                                else:
                                    print("planning to deposit_L1")
                                    robot.navigate.plan_to("deposit_L1")

                        if polarity == "S":
                            if robot.navigate.location != "rack_R_low" and time_deliver_up:
                                if robot.navigate.location == "rack_L_low": # just worth putting in wrong box, and getting back to home
                                    if table["deposit_L2"] == "EMPTY":
                                        print("maximise points: planning to deposit_L2")
                                        robot.navigate.plan_to("deposit_L2")
                                    elif table["deposit_L1"] == "EMPTY":
                                        print("planning to deposit_L1")
                                        robot.navigate.plan_to("deposit_L1")
                                else:
                                    state = "RETURN"

                            else: # do properly
                                if table["deposit_R2"] == "EMPTY":
                                    print("planning to deposit_R2")
                                    robot.navigate.plan_to("deposit_R2")
                                else:
                                    print("planning to deposit_R1")
                                    robot.navigate.plan_to("deposit_R1")

                    print("state = TRAVEL")
                    state = "TRAVEL"
            else:
                robot.follower.step(BASE_SPEED)
                        
        elif state == "DELIVER":

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
                robot.follower.reverse(EXTRA_SLOW_SPEED) 
            while robot.sensors.at_junction() == False:
                robot.follower.reverse(BASE_SPEED)


            if timeup:
                state = "RETURN"

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
                #So we have 3 plans we try in order, then if all else fails a manual reset it is...
                plan = 1 

                if plan == 1:
                    #Try in ten small blocks to go back a bit and see if the sensor error goes away
                    for attempt in range (10):
                        robot.lights.amber_flash(ticks_ms())
                        robot.follower.reverse(SLOW_SPEED)
                        sleep_ms(150)
                        robot.drive.stop()
                        sleep_ms(150)
                        if robot.sensors.error() != None:
                            return
                    plan += 1

                if plan == 2:
                    #Look around you 90 degrees each way and see if you see anything
                    robot.follower.turn("LEFT")
                    robot.follower.turn("180")
                    plan += 1
                
                if plan == 3:
                    #Go forward with caution, letting us intervene if needed
                    robot.follower.step(SLOW_SPEED)
                    sleep_ms(250)
                    pass
      
        elif state == "RETURN": 
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
            state = "TRAVEL"

        elif state == "DONE":
            #print("State is DONE")
            robot.drive.stop()
            robot.lights.amber_off()
            robot.lights.red_off()
            robot.lights.green_off()
            robot.grabber.lower_to_ground()
            robot.grabber.close()
            

        sleep_ms(5)
        t0 = ticks_ms()
        # finetune: only if 2 boxes are delivered, 
        # when 15s left
        # if ticks_diff(t_start, t0) > 255000:
        #     state == "RETURN"


def main():
    """Check if button pressed and then if it is pressed begin the running of the pico routes"""
    if start_pressed(stop_button):
        print("Starting")
        run()

main()