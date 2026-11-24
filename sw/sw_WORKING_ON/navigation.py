"""navigation.py - WHERE to go, kept separate from HOW to drive.

The route is DATA: for each trip, the list of actions to take at successive junctions.
Fill ROUTES by walking the table and counting junctions on the line.
"""

# assume routes from START will start off in the right direction
# assume routes from depos start in right direction
ROUTES = {
    ("START", "rack_L_low"): ["STRAIGHT", "RIGHTTURN", "STRAIGHT", "STRAIGHT"],
    ("START", "rack_R_low"): ["STRAIGHT", "LEFTTURN", "STRAIGHT", "STRAIGHT"],
    ("START", "rack_L_top"): ["WAIT_LIGHTS", "STRAIGHT_RAMP",],
    ("START", "rack_R_top"): ["WAIT_LIGHTS", "STRAIGHT_RAMP"],
    # ("START", "deposit_L1"):["STRAIGHT", "RIGHTTURN", "RIGHTTURN"],
    # ("START", "deposit_L2"):["STRAIGHT", "RIGHTTURN", "STRAIGHT", "RIGHTTURN"],
    # ("START", "deposit_R1"):["STRAIGHT", "LEFTTURN", "LEFTTURN"],
    # ("START", "deposit_R2"):["STRAIGHT", "LEFTTURN", "STRAIGHT", "LEFTTURN"],
    ("rack_L_low", "deposit_L1"): ["STRAIGHT", "LEFTTURN"],
    # ("rack_L_low", "deposit_L2"): ["LEFTTURN"],
    # ("rack_L_low", "START"): ["STRAIGHT", "STRAIGHT", "LEFTTURN", "STRAIGHT"],
    # ("rack_R_low", "deposit_R1"): ["STRAIGHT", "RIGHTTURN"],
    # ("rack_R_low", "deposit_R2"): ["RIGHTTURN"],
    # ("rack_R_low", "START"): ["STRAIGHT", "STRAIGHT", "RIGHTTURN", "STRAIGHT"],
    ("rack_L_top", "START"): ["STRAIGHT"],
    ("rack_L_top", "deposit_L1"): ["LEFTTURN"],
    # ("rack_R_top", "START"): ["STRAIGHT"],
    # ("rack_R_top", "rack_L_top"): [],
    # ("rack_L_top", "rack_R_top"): [],
     ("deposit_L1", "START"): ["LEFTTURN", "STRAIGHT"],
    # ("deposit_L1", "rack_L_low"): ["RIGHTTURN", "STRAIGHT"],
    # ("deposit_L2", "START"): ["LEFTTURN", "STRAIGHT", "LEFTTURN", "STRAIGHT"],
    # ("deposit_L2", "rack_L_low"): ["RIGHTTURN"],
    # ("deposit_R1", "START"): ["RIGHTTURN", "RIGHTTURN", "STRAIGHT"],
    # ("deposit_R1", "rack_R_low"): ["LEFTTURN", "STRAIGHT"],
    # ("deposit_R2", "START"): ["RIGHTTURN", "STRAIGHT", "RIGHTTURN", "STRAIGHT"],
    # ("deposit_R2", "rack_R_low"): ["LEFTTURN"]

    # need to ensure it stops at the end

    
}

class Route:
    def __init__(self):
        self.location = "START" # this is only called when IN the location talked about
        self.lastlocation = "START" # this is only called when deciding what orientation to take at start/ depos
        self.nextlocation = "None" # this is only called for a route split up by "START"
        self._plan = []


    def plan_to(self, destination):
        """This function allows you to specially hardcode a route for testing and can be called by setting destination to LINE_FOLLOWER_TEST in run()"""

        if destination == "LINE_FOLLOWER_TEST": 
            # Prescribed circuit for line follower
            self._plan.extend(ROUTES[(self.location, "rack_R_low")]) # takes to start of left lower rack
            #self._plan.extend(["STRAIGHT", "STRAIGHT", "ABOUTTURN"])
            #self._plan.extend(["STRAIGHT", "STRAIGHT","DOWN_RAMP"])
            self._plan.extend(["LEFTTURNINTOBAY"]) # back to beginning of L low rack
            # self._plan.extend(ROUTES[("rack_L_top", "deposit_L1")]) 
            self._plan.extend(["LEFTTURNINTODEPOSIT"])
            self._plan.extend(ROUTES[("deposit_L1", "START")])
            self._plan.extend(["STOP"])

        else:
            #orientation is variable at "START"
            if self.location == "START":
                if self.lastlocation in ("rack_L_low", "deposit_L1", "deposit_L2"):
                    if destination in ("rack_L_top", "rack_R_top"):
                        print("right start")
                        self._plan.extend(["RIGHTTURN"])

                elif self.lastlocation in ("rack_R_low", "deposit_R1", "deposit_R2"):
                    if destination in ("rack_L_top", "rack_R_top"):
                        self._plan.extend(["LEFTTURN"])
                
                elif self.lastlocation in ("rack_L_top", "rack_R_top"):
                    if destination in ("rack_L_low", "deposit_L1", "deposit_L2"):
                        print("right start")
                        self._plan.extend(["RIGHTTURN"])

                    elif destination in ("rack_R_low", "deposit_R1", "deposit_R2"):
                        self._plan.extend(["LEFTTURN"])

            # orientation is variable at depos (reversing out)
            if self.location in ("deposit_L1", "deposit_L2"):
                if destination == "rack_L_low":
                    self._plan.extend(["LEFTTURN"])
                else:
                    self._plan.extend(["RIGHTTURN"])

            elif self.location in ("deposit_R1", "deposit_R2"):
                if destination == "rack_R_low":
                    self._plan.extend(["RIGHTTTURN"])
                else:
                    self._plan.extend(["LEFTTURN"])


            # actually adding route to plan
            if (self.location, destination) in ROUTES.keys(): # not all routes are in the dictionary so
                self.nextlocation = "None" # so when arrived == TRUE, have actually arrived
                print(f"planning route to {destination}")
                self._plan.append(ROUTES[(self.location, destination)])
                # ahead of time -> TODO: this may be buggy, some code may rely on this being the correct current info
                self.lastlocation = self.location
                self.location = destination
            else:
                self.nextlocation = destination # this is used at end of state = "TRAVEL" to check if there's more to go
                print("planning route to START first")
                self._plan.append(ROUTES[(self.location, "START")])
                # ahead of time
                self.lastlocation = self.location
                self.location = "START"


    def peek_next_move(self):
        return self._plan[0]

    def next_move(self):
        self._plan.pop(0)

    def arrived(self):
        """True when the plan is empty."""
        if len(self._plan) == 0:
            return True
        elif len(self._plan) > 0:
            return False

    # these functions are replaced by dictionary "table"
    
    # def packages_remaining(self):
    #     # 0 = not investigated
    #     # 1 = magnetic box present, taken
    #     # 2 = box present, not magnetic
    #     """TODO: track which racks have been emptied."""
    #     #return edited tuple of 4 lists with 0s, 1s, and 2s: updated as bays searched

    # def depos_remaining(self):
    #     """TODO: track which depos have been filled."""


def turn(drive, sensors, direction, timeout_ms=3000):
    """TODO: drive forward a little so the wheels are over the junction, then spin until
    the centre sensor finds the line again (sensor-based, with a timeout, not a fixed time)."""
