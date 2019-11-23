############ Logging
import sys
f = open('log/media_log.txt', 'w+')
sys.stdout = f


import vlc
import time
import zmq

import config

# Setup media control server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:"+ config.MEDIA_PORT)

# Instance and player
Instance = vlc.Instance(['--video-on-top'])
player = Instance.media_player_new()

# main loop
while True:
    #  Wait for orders
    order = socket.recv()
    if order == config.MEDIA_CMD_TERMINATE:
        exit()

    elif order == config.MEDIA_CMD_STOP:
        print("-- Received a stop order")
        player.stop()
        socket.send(b"OK")

    elif order == config.MEDIA_CMD_PLAY:
        print("-- Received a play order")
        socket.send(b"OK")
        vid_name = socket.recv()
        vid_name = vid_name.decode("utf-8")
        print("-- Playing media at " + vid_name)
        Media = Instance.media_new(vid_name)
        Media.get_mrl()
        player.set_media(Media)
        player.set_fullscreen(True)
        player.play()
        socket.send(b"OK")
