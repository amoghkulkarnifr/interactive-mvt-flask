from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "<p>APIs on /api route<p>"

@app.route("/api/")
def hello_world():
    return {
        "hello": "world"
    }