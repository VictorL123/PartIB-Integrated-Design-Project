"""config.py - every pin and tunable number lives here. Nothing else hardcodes either.

Pins marked KNOWN come from the course example scripts (sw/test_*.py).
Pins marked FILL IN depend on how YOUR robot is wired: check the board labels.
This file deliberately imports nothing from `machine`, so it is plain data.
"""

# ---------------- KNOWN  ----------------
I2C_ID, I2C_SDA, I2C_SCL = 1, 14, 11     # VL53L0X / TCS3472 on I2C0 0,12,14
SERVO_HORIZONTAL_PIN = 13                             # "Servo 1", 50 Hz, 0-270 deg
SERVO_VERTICAL_PIN = 15
ACTUATOR_DIR, ACTUATOR_PWM = 0, 1          # linear actuator on Motor Driv1 #1
START_BUTTON_PIN = 22                      # Pin.IN with PULL_DOWN in the example
# Motor convention in the course Motor class: dir 0 = forward, 1 = reverse

# ---------------- PINS FOR THE PICO ----------------
LEFT_MOTOR_DIR, LEFT_MOTOR_PWM = 4, 5     # e.g. GP4/GP5 is Motor 3
RIGHT_MOTOR_DIR, RIGHT_MOTOR_PWM = 7, 6
LEFT_MOTOR_INVERT = False    # set True if "forward" spins that wheel backwards
RIGHT_MOTOR_INVERT = True   # (motors are mounted mirrored, so one usually needs this)

LINE_SENSOR_PINS = [21,20,19,18]       # left -> right, e.g. (20, 21, 22, 26)
LINE_SENSOR_WEIGHTS = None   # None = auto: 3 sensors -> (-2,0,2), 4 -> (-3,-1,1,3), ...
LINE_ON_VALUE = 1            # what a sensor reads when it is over the line (check!)
LINE_SENSOR_PULL = None      # None, "UP" or "DOWN": depends on the sensor board output

HALL_PIN = 28                            # magnetic field sensor (digital or ADC?)
IR_PIN = 26                             # IR receiver for the traffic light
AMBER_PIN = 8                           # -> optical isolator -> LED
RED_PIN = 10
GREEN_PIN = 9
LED_ON_VALUE = 1             # pin level that lights the LED through your isolator circuit
LED_OFF_VALUE = 0

# ---------------- TUNING FOR LINE SENSING ----------------
DT = 1.5
KP = 12                   # steer harder the further the line is off-centre
KD = 5                    # damps oscillation; raise after KP is tuned
KI = 0

# ---------------- SPEEDS FOR THE MOTOR AND SERVO ----------------

BASE_SPEED = 80           # 0-100
RAMP_SPEED = 90           #Bonus speed to get up the damn ramp
SLOW_SPEED = 30           # approaching packages / ramp
EXTRA_SLOW_SPEED = 45     # Reversing away from / going right up to packages  
SEARCH_SPEED = 30         # pivot speed when the line is lost
SPIN_SPEED = 50

# ---------------- TIMINGS FOR; ----------------

#Turning
LEFT_MOTOR_CORRECTION = 1
TURN_LEFT_90_MS = 2500
TURN_RIGHT_90_MS = 2850
TURN_180_MS = 4000

#Going straight for a time
STRAIGHT_BEFORE_TURN = 750
STRAIGHT_BEFORE_HALFSPIN = 0 # for now
STRAIGHT_TIME_DEPOT = 1100
STRAIGHT_TIME_BAY = 3500
STRAIGHT_TIME_SEARCH = 1700
RAMP_CLOCK_UP = 9000 
RAMP_CLOCK_DOWN = 9000 

#Grabbing times
WAIT_TIME = 3000
FORWARD_BEFORE_GRAB = 1400
FORWARD_BEFORE_DELIVER = 1200
BACK_AFTER_DELIVER = 1000

#Overall competition timings
RUN_TIME_MS = 5 * 60 * 1000
HEAD_HOME_MARGIN_MS = 30 * 1000   # start returning home this long before time is up
LOST_LINE_TIMEOUT_MS = 1500       # give up (and stop) if the line is lost this long

# ---------------- ANGLES FOR THE SERVO ----------------

SERVO_HOR_START_ANGLE = 6
SERVO_VER_START_ANGLE = 180

VER_BOTTOM_RACK_ANGLE = 90 
VER_TOP_ANGLE = 75

HOR_OPEN_ANGLE = 75
HOR_CLOSED_ANGLE = 6

HOR_SPEED_DEG_S = 20
VER_SPEED_DEG_S = 20

# ---------------- CONSTANTS FOR INTERFACING WITH SENSOR DATA ----------------

JUNCTION_CONFIRM = 3      # consecutive readings before we believe a junction
JUNCTION_CROSS_MS = 300   # drive straight this long to get past a junction (tune!)
DEBOUNCE_MS = 25          # button debounce
FLASH_HZ = 2              # amber FLASH rate (on/off cycles per second). Keep it under
                          # 3 Hz and check what the brief's H&S rule wants.
PACKAGE_NEAR_MM = 100      # distance reading that means "block is in the gripper"
PACKAGE_THERE_MM = 200    # distance reading that means "block exists in the bay"
LIFT_TIME_MS = 0          # actuator has no feedback: time the carry height by testing

IR_THREASHOLD = 1
HALL_LOWER_THREASHOLD = 1.75
HALL_UPPER_THREASHOLD = 2.25 #Threasholds for the analogue inputs in voltages

# ---------------- SPECIFIC TEST OPTIONS ----------------
TEST_STOP_AFTER_JUNCTIONS = None  # e.g. 2 = stop after crossing 2 junctions


def require(name, value):
    """Fail early with a readable message if a FILL IN value is still None/empty."""
    if value is None or value == ():
        raise ValueError("config.py: please set " + name)
    return value
