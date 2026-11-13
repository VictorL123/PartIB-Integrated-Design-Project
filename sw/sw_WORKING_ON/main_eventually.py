"""main.py - the state machine ONLY. Aim: fits on 2 sides of A4 (brief requirement).

Each state does one job and names the next state. No pin numbers, no maths in here.
"""
from utime import ticks_ms, sleep_ms, ticks_diff
from config import *
from robot import Robot


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
            robot.navigate.plan_to("LINE_FOLLOWER_TEST")
            t_start = ticks_ms()
            state = "TRAVEL"
        elif state == "TRAVEL":
            # TODO: follower.step(); on junction -> route.next_move() -> turn() or wait_for_green()
            #       if line lost too long -> "RECOVER"; if route.arrived() -> next state
            elapsed = ticks_diff(ticks_ms(),t_start)
            robot.lights.amber_flash(elapsed)
            if robot.sensors.at_junction():
                robot.navigate.next_move()
            robot.follower.step(BASE_SPEED)
            
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
