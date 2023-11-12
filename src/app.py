from flask import Flask

from src.utils.mvt import test__get_max_sharpe

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
    weights = dict(test__get_max_sharpe())
    return {
        "weights": weights
    }
