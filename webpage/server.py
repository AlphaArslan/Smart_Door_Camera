########################## import
from flask import Flask, render_template, redirect, request
import glob
import os
import face_recognition
import pickle

########################## setup
app = Flask(__name__)

########################## file path
slash = "\\"         # windows
# slash = "/"          # linux


known_path = "static" + slash + "known_ppl" + slash
unknown_path = "static" + slash + "unknown_ppl" + slash
log_txt = "static" + slash + "log.txt"


########################## routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/stream')
def strem():
    return render_template("stream.html")

@app.route('/log')
def log():
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


    return render_template("log.html", log = log)

@app.route('/users')
def users():
    known_list = []
    for user in sorted(glob.glob(known_path + '*')):
        # bypass pickle file
        if user.split(".")[-1] == "pickle":
            continue
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
            # bypass pickle file
            if f.split(".")[-1] == "pickle":
                continue
            f_img = face_recognition.load_image_file(f)
            try:
                f_encoding =  face_recognition.face_encodings(f_img)[0]
            except IndexError:
                print("check known images. Aborting...")
                quit()
            known_faces_encodings.append(f_encoding)
        print("saving encodings to file")
        with open(known_path+"encodings.pickle", 'wb') as fp:
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
        # bypass pickle file
        if f.split(".")[-1] == "pickle":
            continue
        f_img = face_recognition.load_image_file(f)
        try:
            f_encoding =  face_recognition.face_encodings(f_img)[0]
        except IndexError:
            print("check known images. Aborting...")
            quit()
        known_faces_encodings.append(f_encoding)

    print("saving encodings to file")
    with open(known_path+"encodings.pickle", 'wb') as fp:
        pickle.dump(known_faces_encodings, fp)

    return redirect('/users')


@app.route("/controls/<string:control>")
def controls(control):
    print(control)
    if control == "open":
        print("opened")
        return "ok"
    return "not found"


########################## main
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
