import RPi.GPIO as GPIO
import config
GPIO.setmode(config.GPIO_MODE)

class PushButton():
    def __init__(self, pin):
        """
        Active High
        """
        GPIO.setup(pin ,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.pin = pin
        self.closed_status = closed_status

    def get_status(self):
        """
        returns True when pressed
        """
        return GPIO.input(self.pin) == self.closed_status
