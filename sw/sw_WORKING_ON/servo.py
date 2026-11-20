from machine import Pin, PWM, ADC
import time
from utime import sleep_ms

class Servo:
    # 6.4V to servo

    # Common settings for 270° servos:
    # 0.5 ms → minimum (0°)
    # 2.5 ms → maximum (270°)
    # Total span = 2.0 ms
    # Frequency: 50 Hz (20 ms period)
    # 
    # Duty % = Pulse width / Period x 100
    # Minimum (0°) = 0.5/20
    # Centre (135°) = 1.5/20
    # Maximum (270°) = 2.5/20
    #
    # Convert to Pico PWM (16-bit)
    # Pico uses: 0 → 65535
    # Duty value = Duty Fraction x 65535
    # Minimum (0.5 ms) = 0.025 * 65535
    # Centre (1.5 ms) = 0.075 * 65535
    # Maximum (2.5 ms) = 0.0125 * 65535
    MIN_DUTY = 1638 # 0°
    MID_DUTY = 4915 # 135°
    MAX_DUTY = 8192 # 270°

    MIN_ADC = 2000       # Raw ADC reading at 0 degrees
    MAX_ADC = 63500      # Raw ADC reading at 270 degrees - need to test and update these!
    
    def __init__(self, ServoPin):
        self.servo = PWM(ServoPin)
        self.servo.freq(50)  # 50 Hz for servo
        # self.servo.adc = ADC(Pin(adc_pin, mode=Pin.IN))
 
    # Convert angle (0–270) to duty
    def set_angle(self, angle):
       # Clamp angle
       if angle < 0:
           angle = 0
       if angle > 270:
           angle = 270
 
       duty = int(Servo.MIN_DUTY + (angle / 270) * (Servo.MAX_DUTY - Servo.MIN_DUTY))
       self.servo.duty_u16(duty)

    def read(self):
        total = 0
        for _ in range(10):
            read = self.servo.adc.read_u16()
            if read == None or read <= 0 or read >= 65535:
                print("No valid servo read")
                return None
            total += read
            time.sleep_ms(2)
        av = total/10
        angle = (av - self.MIN_ADC) * 270.0 / (self.MAX_ADC - self.MIN_ADC)
        return angle


# Test Code
servo1 = Servo(Pin(15)) # Connected to Servo 1
servo2 = Servo(Pin(13))
  
def test_positions():
   #while True:
    print("Move 1")

    # sleep_ms(1000)

    #This code starts the lifting servo in rest and then lifts it up and back down again
    angle = 250
    for i in range(45):
        servo1.set_angle(angle)
        angle -=2
        sleep_ms(75)
    for i in range(45):
        servo1.set_angle(angle)
        angle += 2
        sleep_ms(75)

    angle = 0
    for i in range(45):
        servo2.set_angle(angle)
        angle +=2
        sleep_ms(75)
    for i in range(90):
        servo2.set_angle(angle)
        angle -=2
        sleep_ms(75)
    for i in range(45):
        servo2.set_angle(angle)
        angle += 2
        sleep_ms(75)
 
# Run test
test_positions()
 