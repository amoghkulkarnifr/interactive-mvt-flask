from flask import Flask, abort, request
from pandas import DataFrame

from src.utils.mvt import test__get_max_sharpe
from src.utils.data import get_company_data
from src.utils.mvt.compute import compute__max_sharpe

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
    # _data = get_company_data('ADANIENT')
    _data = get_company_data(['ADANIENT', 'BAJAJ-AUTO', 'CIPLA', 'HCLTECH', 'HDFCBANK'], to_json=True)
    return {
        "status": "OK",
        "data": _data
    }

@app.route("/api/compute")
def api_compute():
    _json_data = request.get_json()
    
    try:
        opt_portfolio = request.args.get('optPortfolio', '', type=str)
    except KeyError as e:
        print('Invalid parameter/s to the compute API')
        abort(400)
    
    if opt_portfolio == "maxSharpeRatio":
        (_weights, _exp_ret, _vol, _sharpe) = compute__max_sharpe(company_names=_json_data['data']['companies'])

        return {
            "status": "OK",
            "data": {
                "weights": _weights,
                "performance": {
                    "expectedReturns": _exp_ret,
                    "volatility": _vol,
                    "sharpeRatio": _sharpe
                }
            }
        }
    else:
        return {
            "status": "OK",
            "data": {}
        }
    
