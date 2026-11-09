"""navigation.py - WHERE to go, kept separate from HOW to drive.

The route is DATA: for each trip, the list of actions to take at successive junctions.
Fill ROUTES by walking the table and counting junctions on the line.
"""

# TODO: fill in from the real table layout. Example shape only:
ROUTES = {
    # ("FROM", "TO"): ["STRAIGHT", "LEFT", "STRAIGHT", ...],
    # ("START", "RACK_A_LOW"): [...],
    # ("RACK_A_LOW", "DEPOT_N"): [...],
}
# Special entries you will probably want: "WAIT_LIGHTS" (traffic lights before top deck)


class Route:
    def __init__(self):
        self.location = "START"
        self._plan = []

    def plan_to(self, destination):
        """TODO: load ROUTES[(self.location, destination)] into self._plan."""

    def next_move(self):
        """TODO: pop and return the next action in the plan."""

    def arrived(self):
        """TODO: True when the plan is empty."""

    def packages_remaining(self):
        """TODO: track which racks have been emptied."""


def turn(drive, sensors, direction, timeout_ms=3000):
    """TODO: drive forward a little so the wheels are over the junction, then spin until
    the centre sensor finds the line again (sensor-based, with a timeout, not a fixed time)."""
