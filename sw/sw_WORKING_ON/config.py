"""config.py - every pin and tunable number lives here. Nothing else hardcodes either.

Pins marked KNOWN come from the course example scripts (sw/test_*.py).
Pins marked FILL IN depend on how YOUR robot is wired: check the board labels.
This file deliberately imports nothing from `machine`, so it is plain data.
"""

# ---------------- KNOWN (course examples) ----------------
I2C_ID, I2C_SDA, I2C_SCL = 0, 8, 9        # VL53L0X / TCS3472 on I2C0
SERVO_PIN = 15                             # "Servo 1", 50 Hz, 0-270 deg
ACTUATOR_DIR, ACTUATOR_PWM = 0, 1          # linear actuator on Motor Driv1 #1
START_BUTTON_PIN = 12                      # Pin.IN with PULL_DOWN in the example
# Motor convention in the course Motor class: dir 0 = forward, 1 = reverse

# ---------------- FILL IN (your wiring) ----------------
LEFT_MOTOR_DIR, LEFT_MOTOR_PWM = 7, 6     # e.g. GP4/GP5 is Motor 3
RIGHT_MOTOR_DIR, RIGHT_MOTOR_PWM = 4, 5
LEFT_MOTOR_INVERT = False    # set True if "forward" spins that wheel backwards
RIGHT_MOTOR_INVERT = False   # (motors are mounted mirrored, so one usually needs this)

LINE_SENSOR_PINS = [8,9,10,11]       # left -> right, e.g. (20, 21, 22, 26)
LINE_SENSOR_WEIGHTS = None   # None = auto: 3 sensors -> (-2,0,2), 4 -> (-3,-1,1,3), ...
LINE_ON_VALUE = 1            # what a sensor reads when it is over the line (check!)
LINE_SENSOR_PULL = None      # None, "UP" or "DOWN": depends on the sensor board output

HALL_PIN = None                            # magnetic field sensor (digital or ADC?)
IR_PIN = None                              # IR receiver for the traffic light
AMBER_PIN = None                           # -> optical isolator -> LED
RED_PIN = None
GREEN_PIN = None
LED_ON_VALUE = 1             # pin level that lights the LED through your isolator circuit

# ---------------- TUNING ----------------
DT = 1.5
BASE_SPEED = 100           # 0-100
SLOW_SPEED = 30           # approaching packages / ramp
SEARCH_SPEED = 30         # pivot speed when the line is lost
KP = 8                   # steer harder the further the line is off-centre
KD = 2                    # damps oscillation; raise after KP is tuned
KI = 0
JUNCTION_CONFIRM = 3      # consecutive readings before we believe a junction
JUNCTION_CROSS_MS = 300   # drive straight this long to get past a junction (tune!)
DEBOUNCE_MS = 25          # button debounce
FLASH_HZ = 2              # amber FLASH rate (on/off cycles per second). Keep it under
                          # 3 Hz and check what the brief's H&S rule wants.
PACKAGE_NEAR_MM = 60      # distance reading that means "block is in the gripper"
LIFT_TIME_MS = 0          # actuator has no feedback: time the carry height by testing
RUN_TIME_MS = 5 * 60 * 1000
HEAD_HOME_MARGIN_MS = 30 * 1000   # start returning home this long before time is up
LOST_LINE_TIMEOUT_MS = 1500       # give up (and stop) if the line is lost this long

# ---------------- bench-test options (line_test.py only) ----------------
TEST_STOP_AFTER_JUNCTIONS = None  # e.g. 2 = stop after crossing 2 junctions


def require(name, value):
    """Fail early with a readable message if a FILL IN value is still None/empty."""
    if value is None or value == ():
        raise ValueError("config.py: please set " + name)
    return value
