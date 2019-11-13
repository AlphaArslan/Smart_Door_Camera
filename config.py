import RPi.GPIO as GPIO

DEBUG_MODE = True

########################### pin config GPIO.BOARD
GPIO_MODE           =       GPIO.BOARD

BELL_PIN            =       29
LOCK_PIN            =       7

########################### time delays [in secends]
BELL_CHECK_DELAY    =       0.2
OPEN_LOCK_DELAY     =       2

########################### media commands
MEDIA_CMD_PLAY      =       b'play'
MEDIA_CMD_STOP      =       b'stop'
MEDIA_CMD_TERMINATE =       b'terminate'
MEDIA_PORT          =       "4456"

########################### tolerance
FACE_TOLERANCE      =       0.6             # 0.6 default .. less is more strict
