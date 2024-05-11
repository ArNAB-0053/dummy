from flask import Flask
app = Flask(__name__)

a = 5
b = 6

@app.route('/')
def hello_world():
    res = {
        "a": a,
        "b":b
    }
    return res
