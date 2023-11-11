from flask import Flask
from .utils.mvt.test import get_max_sharpe

app = Flask(__name__)

@app.route("/")
def root():
    return "<p>APIs on /api route<p>"

@app.route("/api/")
def api_list():
    return {
        "test": "max sharpe portfolio on test data"
    }

@app.route("/api/test")
def api_test():
    weights = get_max_sharpe()
    print(weights)
    return {
        "weights": weights
    }
