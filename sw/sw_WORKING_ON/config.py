"""config.py - every pin and tunable number lives here. Nothing else hardcodes either.

Pins marked KNOWN come from the course example scripts (sw/test_*.py).
Pins marked FILL IN depend on how YOUR robot is wired: check the board labels.
"""

# ---------------- KNOWN (course examples) ----------------
I2C_ID, I2C_SDA, I2C_SCL = 0, 8, 9        # VL53L0X / TCS3472 on I2C0
SERVO_PIN = 15                             # "Servo 1", 50 Hz, 0-270 deg
ACTUATOR_DIR, ACTUATOR_PWM = 0, 1          # linear actuator on Motor Driv1 #1
START_BUTTON_PIN = 12                      # Pin.IN with PULL_DOWN in the example
# Motor convention in the course Motor class: dir 0 = forward, 1 = reverse

# ---------------- FILL IN (your wiring) ----------------
LEFT_MOTOR_DIR, LEFT_MOTOR_PWM = None, None     # e.g. GP4/GP5 is Motor 3
RIGHT_MOTOR_DIR, RIGHT_MOTOR_PWM = None, None
LINE_SENSOR_PINS = ()                      # left -> right
LINE_SENSOR_WEIGHTS = ()                   # e.g. (-3, -1, 1, 3) for 4 sensors
LINE_ON_VALUE = 1                          # what a sensor reads over the line (check!)
HALL_PIN = None                            # magnetic field sensor (digital or ADC?)
IR_PIN = None                              # IR receiver for the traffic light
AMBER_PIN = None                           # -> optical isolator -> LED
RED_PIN = None
GREEN_PIN = None

# ---------------- TUNING ----------------
BASE_SPEED = 50           # 0-100
SLOW_SPEED = 30           # approaching packages / ramp
KP = 12
KD = 8
JUNCTION_CONFIRM = 3      # consecutive readings before we believe a junction
FLASH_HZ = 2              # timer toggles at this rate -> check H&S flash rate in the brief
PACKAGE_NEAR_MM = 60      # distance reading that means "block is in the gripper"
LIFT_TIME_MS = 0          # actuator has no feedback: time the carry height by testing
RUN_TIME_MS = 5 * 60 * 1000
HEAD_HOME_MARGIN_MS = 30 * 1000   # start returning home this long before time is up
LOST_LINE_TIMEOUT_MS = 1500
