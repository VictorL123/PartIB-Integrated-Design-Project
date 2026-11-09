"""main.py - the state machine ONLY. Aim: fits on 2 sides of A4 (brief requirement).

Each state does one job and names the next state. No pin numbers, no maths in here.
"""
import time
from config import *
from motors import Motor, Drivetrain
from line_sensors import LineSensors
from line_follow import LineFollower
from navigation import Route, turn
from distance import DistanceSensor
from grabber import Grabber
from magnet import read_polarity
from lights import Lights
from ir_receiver import wait_for_green
from buttons import start_pressed, stop_pressed


def build_robot():
    """TODO: create every object once and return them (or put them in a dict)."""


def run():
    # TODO: robot = build_robot()
    state = "WAIT_START"
    t_start = 0

    while True:
        # --- safety first, every loop ---
        # TODO: if stop_pressed(): stop motors, lights off, state = "WAIT_START"
        # TODO: if time is nearly up and state is not RETURN/DONE: plan_to("START"), state = "RETURN"

        if state == "WAIT_START":
            # TODO: wait for start_pressed(); record t_start; amber flash on; plan first trip
            pass
        elif state == "TRAVEL":
            # TODO: follower.step(); on junction -> route.next_move() -> turn() or wait_for_green()
            #       if line lost too long -> "RECOVER"; if route.arrived() -> next state
            pass
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

        time.sleep_ms(5)


try:
    run()
finally:
    # Whatever goes wrong, leave the robot safe. TODO: stop motors, actuator, lights.
    pass
