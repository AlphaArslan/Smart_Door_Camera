########################## import
from flask import Flask, render_template, redirect, request
import glob
import os
import face_recognition
import pickle
from time import sleep

from sys import path
path.append('..')
import config
import relay

########################## setup
app = Flask(__name__)
lock_obj = relay.Relay(config.LOCK_PIN)

########################## file path
# slash = "\\"         # windows
slash = "/"          # linux


known_path = "static" + slash + "known_ppl" + slash
unknown_path = "static" + slash + "unknown_ppl" + slash
log_txt = "static" + slash + "log.txt"
enc_pickle = "webpage" + slash + "static" + slash + "known_faces_encodings.pickle"


########################## routes
# no cache
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/stream')
def stream():
    imgs = sorted(glob.glob(unknown_path + '*'))
    if len(imgs) > 0:
        img = imgs[-1].split(slash)[-1]
    else:
        img = "no_image.jpg"
    return render_template("stream.html", img = img)

@app.route('/log')
def log():
    try:
        with open(log_txt, "r") as log:
            log_lines = log.readlines()
            log_lines.reverse()
        log = []
        for line in log_lines:
            _a = line.split(" ")
            # known
            if _a[0] == "Allowed":
                _img = "static/known_ppl/{}.jpg".format(_a[1])
            # unknown
            elif _a[0] == "Rejected":
                _img = "static/unknown_ppl/{}.jpg".format(_a[1])
            log.append((_img, line))

    except :
        log = [("_", "No log yet")]

    return render_template("log.html", log = log)

@app.route('/users')
def users():
    known_list = []
    for user in sorted(glob.glob(known_path + '*')):
        name = user.split(slash)[-1].split('.')[0]
        known_list.append(name)
    unknown_list = []
    for user in sorted(glob.glob(unknown_path + '*')):
        name = user.split(slash)[-1].split('.')[0]
        unknown_list.append(name)
    return render_template("users.html", known_list = known_list, unknown_list = unknown_list)


@app.route('/remove/<string:k>/<string:name>')
def remove(k, name):
    if k == 'known':
        os.remove(known_path+name+'.jpg')
        print("proccessing known images encodings")
        known_faces_encodings = []
        known_faces = sorted(glob.glob(known_path+'*'))
        for f in known_faces:
            f_img = face_recognition.load_image_file(f)
            try:
                f_encoding =  face_recognition.face_encodings(f_img)[0]
            except IndexError:
                print("check known images. Aborting...")
                quit()
            known_faces_encodings.append(f_encoding)
        print("saving encodings to file")
        with open(enc_pickle, 'wb') as fp:
            pickle.dump(known_faces_encodings, fp)

    elif k == 'unknown':
        os.remove(unknown_path+name+'.jpg')

    return redirect('/users')


@app.route('/add_user/<string:old_name>', methods=['GET', 'POST'])
def add_user(old_name):
    name = request.form["name"]
    os.rename(unknown_path+old_name+'.jpg',known_path+name+'.jpg')

    print("proccessing known images encodings")
    known_faces_encodings = []
    known_faces = sorted(glob.glob(known_path+'*'))
    for f in known_faces:
        f_img = face_recognition.load_image_file(f)
        try:
            f_encoding =  face_recognition.face_encodings(f_img)[0]
        except IndexError:
            print("check known images. Aborting...")
            quit()
        known_faces_encodings.append(f_encoding)

    print("saving encodings to file")
    with open(enc_pickle, 'wb') as fp:
        pickle.dump(known_faces_encodings, fp)

    return redirect('/users')


@app.route("/controls/<string:control>")
def controls(control):
    print(control)
    if control == "open":
        # open lock
        lock_obj.on()

        sleep(config.OPEN_LOCK_DELAY)

        # close lock
        lock_obj.off()

        print("opened")
        return "ok"
    return "not found"


########################## main
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
