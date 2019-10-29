import sys
sys.path.append('..')

import push_button
import config

import time

pb = push_button.PushButton(config.BELL_PIN)

while true:
    print(pb.get_status())
    time.sleep(1)
