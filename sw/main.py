#from test_led import test_led
#from test_led_pwm import test_led_pwm
from test_motor import test_motors
#from test_tcs3472 import test_tcs3472
from Distance_sensor_test import test_vl53l0x
from Drive_motors import test_drive


print("Welcome to main.py!")

# Uncomment the test to run
# test_led()
# test_led_pwm()
#test_motors()
# test_tcs3472()
#test_vl53l0x()
test_drive()

print("main.py Done!")
