########################## import
from flask import Flask, render_template


########################## setup
app = Flask(__name__)



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
    return render_template("users.html")


########################## main
if __name__ == '__main__':
    app.run(debug=True)
