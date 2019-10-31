########################## import
from flask import Flask, render_template, redirect, request
import glob
import os

########################## setup
app = Flask(__name__)

########################## file path
slash = "\\"         # windows
# slash = "/"          # linux


known_path = "static" + slash + "known_ppl" + slash
unknown_path = "static" + slash + "unknown_ppl" + slash



########################## routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/stream')
def strem():
    return render_template("stream.html")

@app.route('/log')
def log():
    return render_template("log.html")

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
    elif k == 'unknown':
        os.remove(unknown_path+name+'.jpg')
    return redirect('/users')


@app.route('/add_user/<string:old_name>', methods=['GET', 'POST'])
def add_user(old_name):
    name = request.form["name"]
    os.rename(unknown_path+old_name+'.jpg',known_path+name+'.jpg')
    return redirect('/users')


########################## main
if __name__ == '__main__':
    app.run(debug=True)
