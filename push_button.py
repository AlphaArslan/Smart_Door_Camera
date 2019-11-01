import RPi.GPIO as GPIO
import config
import time

GPIO.setmode(config.GPIO_MODE)

class PushButton():
    def __init__(self, pin):
        """
        Active High
        """
        GPIO.setup(pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pin = pin
        self.closed_status = 0

    def is_pressed(self):
        """
        returns True when pressed
        """
        return GPIO.input(self.pin) == self.closed_status

############################ test
if __name__ == '__main__':
    pb = PushButton(config.BELL_PIN)
    while True:
        print(pb.get_status())
        time.sleep(1)
