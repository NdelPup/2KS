import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class led ():

    def led_verde(self):
        GPIO.setup(18,GPIO.OUT)
        GPIO.output(18,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(18,GPIO.LOW)

    def led_verde_on(self):
        GPIO.setup(18,GPIO.OUT)
        GPIO.output(18,GPIO.HIGH)

    def led_verde_off(self):
        GPIO.setup(18,GPIO.OUT)
        GPIO.output(18,GPIO.LOW)

        
    def led_rosso(self):
        GPIO.setup(23,GPIO.OUT)
        GPIO.output(23,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(23,GPIO.LOW)

    def led_rosso_on(self):
        GPIO.setup(23,GPIO.OUT)
        GPIO.output(23,GPIO.HIGH)
        
    def led_rosso_off(self):
        GPIO.setup(23,GPIO.OUT)
        GPIO.output(23,GPIO.LOW)

    def led_rosso_blink(self):
        GPIO.setup(23,GPIO.OUT)
        for count in range (1, 10):
            GPIO.output(23, GPIO.LOW)  # led off
            time.sleep(0.2)
            GPIO.output(23, GPIO.HIGH) # led on
            time.sleep(0.2)
            GPIO.output(23, GPIO.LOW)  # led off
            time.sleep(0.2)


    def led_giallo(self):
        GPIO.setup(25,GPIO.OUT)
        GPIO.output(18,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(25,GPIO.LOW)

    def led_giallo_on(self):
        GPIO.setup(25,GPIO.OUT)
        GPIO.output(25,GPIO.HIGH)
        
    def led_giallo_off(self):
        GPIO.setup(25,GPIO.OUT)
        GPIO.output(25,GPIO.LOW)

    def led_giallo_blink(self):
        GPIO.setup(25,GPIO.OUT)
        for count in range (1, 10):
            GPIO.output(25, GPIO.HIGH)  # led on
            time.sleep(0.1)
            GPIO.output(25, GPIO.LOW) # led off
            time.sleep(0.1)
            

    def led_bianco(self):
        GPIO.setup(12,GPIO.OUT)
        GPIO.output(12,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(12,GPIO.LOW)
        
    def led_bianco_on(self):
        GPIO.setup(12,GPIO.OUT)
        GPIO.output(12,GPIO.HIGH)
        
    def led_bianco_off(self):
        GPIO.setup(12,GPIO.OUT)
        GPIO.output(12,GPIO.LOW)
        
    def led_bianco_blink(self):
        GPIO.setup(12,GPIO.OUT)
        for count in range (1, 10):
            GPIO.output(12, GPIO.LOW)  # led off
            time.sleep(0.1)
            GPIO.output(12, GPIO.HIGH) # led on
            time.sleep(0.1)


    def ledStart(self):
        self.led_verde_on()
        time.sleep(0.5)
        self.led_rosso_on()
        time.sleep(0.5)
        self.led_giallo_on()
        time.sleep(0.5)
        self.led_bianco_on()
        time.sleep(0.5)
        self.led_verde_off()
        time.sleep(0.5)
        self.led_rosso_off()
        time.sleep(0.5)
        self.led_giallo_off()
        time.sleep(0.5)
        self.led_bianco_off()
        self.led_bianco_blink()
        self.led_bianco_on
