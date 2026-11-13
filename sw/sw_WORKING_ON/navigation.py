"""navigation.py - WHERE to go, kept separate from HOW to drive.

The route is DATA: for each trip, the list of actions to take at successive junctions.
Fill ROUTES by walking the table and counting junctions on the line.
"""
from robot import Robot
from config import BASE_SPEED, SPIN_SPEED
import time

# bays_l_low = [0] * 6
# bays_r_low = [0] * 6
# bays_l_top = [0] * 6
# bays_l_top = [0] * 6

# TODO: fill in from the real table layout
# assume routes starting from START will start off in the right direction
ROUTES = {
    ("START", "rack_L_low"): ["STRAIGHT", "STRAIGHT", "RIGHTTURN", "STRAIGHT", "STRAIGHT", "STRAIGHT"],
    ("START", "rack_r_low"): ["STRAIGHT", "STRAIGHT", "LEFTTURN", "STRAIGHT", "STRAIGHT", "STRAIGHT"],
    ("START", "rack_top"): ["STRAIGHT", "WAIT_LIGHTS", "STRAIGHT"],
    # ("START", "deposit_L1"):[]
    # ("START", "deposit_L2"):[]
    # ("START", "deposit_R1"):[]
    # ("START", "deposit_R2"):[]
    ("rack_L_low", "deposit_L1"): ["STRAIGHT", "STRAIGHT", "LEFTTURN"],
    # ("rack_L_low", "deposit_L2"): ["STRAIGHT", "LEFTTURN"],
    # ("rack_L_low", "START"): ["STRAIGHT", "STRAIGHT", "STRAIGHT", "LEFTTURN", "STRAIGHT", "STRAIGHT"],
    # ("rack_R_low", "deposit_R1"): ["STRAIGHT", "STRAIGHT", "RIGHTTURN"],
    # ("rack_R_low", "deposit_R2"): ["STRAIGHT, RIGHTTURN"],
    # ("rack_R_low", "START"): ["STRAIGHT", "STRAIGHT", "STRAIGHT", "RIGHTTURN", "STRAIGHT", "STRAIGHT"],
    # ("rack_top", "START"): ["STRAIGHT", "STRAIGHT"],
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
        self.lastlocation = "START"
        #for the line follower test, this will not change (since the movements are prescribed, it doesn't need to)
        self._plan = []
        self._arrived = False


    def plan_to(self, destination):
        """TODO: load ROUTES[(self.location, destination)] into self._plan."""
        if destination == "LINE_FOLLOWER_TEST": 
            # Prescribed circuit for line follower
            self._plan.extend(["LEFTTURN"])
            self._plan.extend(ROUTES[(self.location, "rack_L_low")]) # takes to start of left lower rack
            self._plan.extend(["STRAIGHT", "RIGHTTURN", "STRAIGHT1S", "WAIT2S", "ABOUTTURN", "STRAIGHT", "LEFTTURN", "STRAIGHT"]) # back to beginning of L low rack
            self._plan.extend(ROUTES[("rack_L_low", "deposit_L1")]) #
            self._plan.extend(["STRAIGHT1S", "WAIT2S", "ABOUTTURN", "STRAIGHT"])
            self._plan.extend(ROUTES[("deposit_L1", "START")])
            self._plan.extend(["STOP"])

        else:
            #orientation is variable at "START"
            if self.location == "START":
                if self.lastlocation in ("rack_L_low", "deposit_L1", "deposit_L2"):
                    if destination == "rack_top":
                        self._plan.extend(["RIGHTTURN"])

                elif self.lastlocation in ("rack_R_low", "deposit_R1", "deposit_R2"):
                    if destination == "rack_top":
                        self._plan.extend(["LEFTTURN"])
                
                elif self.lastlocation == "rack_top":
                    if destination in ("rack_L_low", "deposit_L1", "deposit_L2"):
                        self._plan.extend(["RIGHTTURN"])

                    if destination in ("rack_R_low", "deposit_R1", "deposit_R2"):
                        self._plan.extend(["LEFTTURN"])

               
            self._plan.append(ROUTES[(self.location, destination)])

    def next_move(self):
        """TODO: pop and return the next action in the plan."""
        # run the next move (first in self._plan), then pop it
        move = self._plan[0]
        robot = Robot()
        if move == "STRAIGHT":
            robot.follower.step(BASE_SPEED)

        if move == "STRAIGHT1S":
            t_end = time.time() + 1
            while time.time() < t_end:
                robot.follower.step(BASE_SPEED)

        elif move == "LEFTTURN":
            robot.follower.turn("LEFT", SPIN_SPEED)

        elif move == "RIGHTTURN":
            robot.follower.turn("RIGHT", SPIN_SPEED)

        elif move == "ABOUTTURN":
            robot.follower.turn("180", SPIN_SPEED)
            
        elif move == "WAIT2S":
            t_end = time.time() + 2
            while time.time() < t_end:
                robot.drive.stop()

        elif move == "STOP":
            robot.drive.stop()

        self._plan.pop(0)

            # should break but not stop moving when meets junction


    def arrived(self, destination):
        """TODO: True when the plan is empty."""
        if len(self._plan) < 1:
            self._arrived = True
            self.lastlocation = self.location
            self.location = destination
        elif len(self._plan) > 0:
            self._arrived = False

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
