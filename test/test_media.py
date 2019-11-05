import zmq
import time
import sys
sys.path.append('..')

import config

# socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:"+config.MEDIA_PORT)

socket.send(config.MEDIA_CMD_STOP)
print(socket.recv())
# send play command
socket.send(config.MEDIA_CMD_PLAY)
print(socket.recv())
socket.send("voice\\cant_see.m4a".encode('utf-8'))
print(socket.recv())
# input("press any key to stop media")
time.sleep(8)
socket.send(config.MEDIA_CMD_STOP)
print(socket.recv())

# input("press any key to terminate")
# socket.send(config.MEDIA_CMD_TERMINATE)
