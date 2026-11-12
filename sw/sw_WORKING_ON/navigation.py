"""navigation.py - WHERE to go, kept separate from HOW to drive.

The route is DATA: for each trip, the list of actions to take at successive junctions.
Fill ROUTES by walking the table and counting junctions on the line.
"""
from robot import Robot
from config import BASE_SPEED
from utime import sleep

# bays_l_low = [0] * 6
# bays_r_low = [0] * 6
# bays_l_top = [0] * 6
# bays_l_top = [0] * 6

# TODO: fill in from the real table layout. Example shape only:
ROUTES = {
    ("START", "rack_L_low"): ["LEFTTURN", "STRAIGHT", "STRAIGHT", "RIGHTTURN", "STRAIGHT", "STRAIGHT", "STRAIGHT"],
    ("START", "rack_r_low"): ["RIGHTTURN", "STRAIGHT", "STRAIGHT", "LEFTTURN", "STRAIGHT", "STRAIGHT", "STRAIGHT"],
    ("START", "rack_top"): ["STRAIGHT", "WAIT_LIGHTS", "STRAIGHT"],
    # ("START", "deposit_L1"):[]
    # ("START", "deposit_L2"):[]
    # ("START", "deposit_R1"):[]
    # ("START", "deposit_R2"):[]
    ("rack_L_low", "deposit_L1"): ["STRAIGHT", "STRAIGHT", "LEFTTURN"],
    # ("rack_L_low", "deposit_L2"): []
    # ("rack_L_low", "START"): []
    # ("rack_R_low", "deposit_R1"): []
    # ("rack_R_low", "deposit_R2"): []
    # ("rack_R_low", "START"): []
    # ("rack_top", "START"): []
    ("deposit_L1", "START"): ["LEFTTURN", "STRAIGHT", "STRAIGHT", "LEFTTURN", "STRAIGHT", "STRAIGHT"]
    # ("deposit_L1", "rack_L_low"): []
    # ("deposit_L2", "START"): []
    # ("deposit_L2", "rack_L_low"): []
    # ("deposit_R1", "START"): []
    # ("deposit_R1", "rack_R_low"): []
    # ("deposit_R2", "START"): []
    # ("deposit_R2", "rack_R_low"): []

    # need to ensure it stops at the end

    
}
# Special entries you will probably want: "WAIT_LIGHTS" (traffic lights before top deck)
#how to count junctions?? how to put that information here


class Route:
    def __init__(self):
        self.location = "START"
        self._plan = []


    def plan_to(self, destination):
        """TODO: load ROUTES[(self.location, destination)] into self._plan."""
        if destination == "LINE_FOLLOWER_TEST": 
             self._append(ROUTES[(self.location, "rack_L_low")]) # takes to start of left lower rack
             self._append["STRAIGHT", "RIGHTTURN", "1s_STRAIGHT", "WAIT2S", "ABOUTTURN", ]
             self._append(ROUTES[("rack_L_low", "")])
        else:
            self._plan.append(ROUTES[(self.location, destination)])

    def next_move(self):
        """TODO: pop and return the next action in the plan."""
        # run the next move (first in self._plan), then pop it
        move = self._plan(0)
        robot = Robot()
        if move == "STRAIGHT":
            robot.follower.step(BASE_SPEED)
            pass
        if move == "1s_STRAIGHT":
            # ** how to travel for 1 second?
            robot.follower.step(BASE_SPEED)
            pass
        elif move == "LEFTTURN":
            robot.follower.turn(BASE_SPEED, "LEFT")
            pass
        elif move == "RIGHTTURN":
            robot.follower.turn(BASE_SPEED, "RIGHT")
            pass
        elif move == "ABOUTTURN":
            robot.follower.turn(BASE_SPEED, "180")
            pass
        elif move == "WAIT2S":
            sleep(2)
            pass
        self._plan.pop(0)


        

            # should break but not stop moving when meets junction





    def arrived(self):
        """TODO: True when the plan is empty."""
        #at the end of that chosen entry from ROUTES

    def packages_remaining(self):
        # 0 = not investigated
        # 1 = magnetic box present, taken
        # 2 = box present, not magnetic
        """TODO: track which racks have been emptied."""
        #return edited tuple of 4 lists with 0s, 1s, and 2s: updated as bays searched

    def depos_remaining(self):
        """TODO: track which depos have been filled."""


def turn(drive, sensors, direction, timeout_ms=3000):
    """TODO: drive forward a little so the wheels are over the junction, then spin until
    the centre sensor finds the line again (sensor-based, with a timeout, not a fixed time)."""
