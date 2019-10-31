import RPi.GPIO as GPIO
import config
GPIO.setmode(config.GPIO_MODE)
GPIO.setwarnings(False)

class Output():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def high(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def low(self):
        GPIO.output(self.pin, GPIO.LOW)
