from flask import Flask

from src.utils.mvt import test__get_max_sharpe
from src.utils.data import get_company_data

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

@app.route("/api/data")
def api_get_data():
    # _data = compute_max_sharpe('ADANIENT')
    _data = get_company_data(['ADANIENT', 'BAJAJ-AUTO', 'CIPLA', 'HCLTECH', 'HDFCBANK'])
    return {
        "data": _data
    }
