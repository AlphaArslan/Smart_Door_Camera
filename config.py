import RPi.GPIO as GPIO

DEBUG_MODE = True

########################### pin config GPIO.BOARD
GPIO_MODE           =       GPIO.BOARD

BELL_PIN            =       29
LOCK_PIN            =       7

########################### time delays [in secends]
BELL_CHECK_DELAY    =       0.2
OPEN_LOCK_DELAY     =       2
