from machine import Pin, PWM
from utime import sleep

class Drive:
    #Take the input pins of both motors and allow them to drive together as one system
    def __init__(self, directionPin1, PWMPin1, directionPin2, PWMPin2): #PWM = pulse-width modulation and describes inputing a square wave to lower average pin volatage
        self.mDir1 = Pin(directionPin1, Pin.OUT)  # set motor direction pin1
        self.pwm1 = PWM(Pin(PWMPin1))  # set motor pwm pin1
        self.mDir2 = Pin(directionPin2, Pin.OUT)  # set motor direction pin2
        self.pwm2 = PWM(Pin(PWMPin2))  # set motor pwm pin2
        self.pwm1.freq(1000)
        self.pwm2.freq(1000)# set PWM frequency
        self.pwm1.duty_u16(0)  # set duty cycle - 0=off
        self.pwm2.duty_u16(0)

    def off(self):
        self.pwm1.duty_u16(0)
        self.pwm2.duty_u16(0)

    def Forward(self, speedL=100, speedR=100):
        self.mDir1.value(0) # forward = 0; reverse = 1 motor
        self.pwm1.duty_u16(int(65535 * speedL / 100))
        self.mDir2.value(0)                   
        self.pwm2.duty_u16(int(65535 * speedR / 100))  # speed range; 0-100 motor

    def Reverse(self, speedL=30, speedR=30):
        self.mDir1.value(1) #set the motor in reverse
        self.pwm1.duty_u16(int(65535 * speedL / 100))
        self.mDir2.value(1)
        self.pwm2.duty_u16(int(65535 * speedR / 100))

def test_drive():
    motors = Drive(4,5,7,6)

    for _ in range(10):
        print("Forward")
        motors.Forward(50,50)
        sleep(1)
        print("Reverse")
        motors.Reverse(50,50)
        sleep(1)
        motors.off()	

if __name__ == "__main__":
    test_drive()

    


