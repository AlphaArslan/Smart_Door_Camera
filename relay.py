import RPi.GPIO as GPIO
import config
GPIO.setmode(config.GPIO_MODE)


class Relay():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

####################################
if __name__ == '__main__':
    from time import sleep
    r = Relay(config.LOCK_PIN)
    r.on()
    sleep(5)
    r.off()
