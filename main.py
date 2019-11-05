################### Import
import time
import face_recognition
import glob
import pickle
import cv2
import zmq

import config
import push_button
import pins
import camera
import relay

################### objects
bell_obj = push_button.PushButton(config.BELL_PIN)
cam_obj = camera.Camera(0)
lock_obj = relay.Relay(config.LOCK_PIN)
# socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:"+config.MEDIA_PORT)

################### path
slash = '\\'                # windows
# slash = '/'                # linux

known_path = "webpage" + slash + "static" + slash + "known_ppl" + slash
unknown_path = "webpage" + slash + "static" + slash + "unknown_ppl" + slash

################### func
def open_lock():
    # open
    lock_obj.on()
    # delay
    time.sleep(config.OPEN_LOCK_DELAY)
    # close
    lock_obj.off()

################### main
if __name__ == '__main__':
    # setup
    unknown_counter = len(glob.glob(unknown_path+'*'))
    allowed = False
    print("[SETUP] proccessing known images encodings")
    known_faces_encodings = []
    known_faces = sorted(glob.glob(known_path+'*'))
    for f in known_faces:
        # bypass pickle file
        if f.split(".")[-1] == "pickle":
            continue
        f_img = face_recognition.load_image_file(f)
        try:
            f_encoding =  face_recognition.face_encodings(f_img)[0]
        except IndexError:
            print("[SETUP] check known images. Aborting...")
            quit()
        known_faces_encodings.append(f_encoding)

    print("[SETUP] saving encodings to file")
    with open(known_path+"encodings.pickle", 'wb') as fp:
        pickle.dump(known_faces_encodings, fp)

    # loop
    while True:
        # wait for door bell
        if config.DEBUG_MODE:
            print("[LOOP] Waiting for bell ring ...")
        while not bell_obj.is_pressed():
            time.sleep(config.BELL_CHECK_DELAY)

        # take a pic
        if config.DEBUG_MODE:
            print("[LOOP] Taking a pic")
        img = cam_obj.get_image()
        try:
            img_encoding = face_recognition.face_encodings(img)[0]
        except IndexError:
            print("[LOOP] camera can't see anyone")
            # play voice
            socket.send(config.MEDIA_CMD_STOP)
            print(socket.recv())
            # send play command
            socket.send(config.MEDIA_CMD_PLAY)
            print(socket.recv())
            socket.send("voice\\cant_see.m4a".encode('utf-8'))
            print(socket.recv())
            # input("press any key to stop media")
            time.sleep(1)
            socket.send(config.MEDIA_CMD_STOP)
            print(socket.recv())

            continue

        # check if allowed
        if config.DEBUG_MODE:
            print("[LOOP] Check if allowed")
        with open (known_path+"encodings.pickle", 'rb') as fp:
            known_faces_encodings = pickle.load(fp)
        results = face_recognition.compare_faces(known_faces_encodings, img_encoding)
        for r in results:
            if r :
                allowed = True
                break

        # if allowed open
        if allowed:
            if config.DEBUG_MODE:
                print("[LOOP] allowed")

            # play voice
            socket.send(config.MEDIA_CMD_STOP)
            print(socket.recv())
            # send play command
            socket.send(config.MEDIA_CMD_PLAY)
            print(socket.recv())
            socket.send("voice\\allowed.m4a".encode('utf-8'))
            print(socket.recv())
            # input("press any key to stop media")
            time.sleep(1)
            socket.send(config.MEDIA_CMD_STOP)
            print(socket.recv())

            # add to log

            open_lock()
            allowed = False
        # if not allowed add to unkown
        else:
            if config.DEBUG_MODE:
                print("[LOOP] not allowed")
            unknown_counter += 1

            # play voice
            socket.send(config.MEDIA_CMD_STOP)
            print(socket.recv())
            # send play command
            socket.send(config.MEDIA_CMD_PLAY)
            print(socket.recv())
            socket.send("voice\\not_allowed.m4a".encode('utf-8'))
            print(socket.recv())
            # input("press any key to stop media")
            time.sleep(1)
            socket.send(config.MEDIA_CMD_STOP)
            print(socket.recv())

            # add to log

            # send email

            cv2.imwrite(unknown_path+"unknown{}.jpg".format(unknown_counter), img)
