from time import sleep
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class buzzer:
    
    def buzz(self):
        buzzTime = 1

        buzzPin = 20  #numero del pin

        GPIO.setup(buzzPin, GPIO.OUT)

        GPIO.output(buzzPin, True)
        sleep(buzzTime)
        GPIO.output(buzzPin, False)

