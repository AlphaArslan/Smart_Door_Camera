import RPi.GPIO as GPIO
import config
GPIO.setmode(config.GPIO_MODE)

class PushButton():
    def __init__(self, pin, closed_status = 1):
        GPIO.setup(pin ,GPIO.IN)
        self.pin = pin
        self.closed_status = closed_status

    def get_status(self):
        return GPIO.input(DETECTOR) == self.closed_status
