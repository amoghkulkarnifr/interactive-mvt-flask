from flask import Flask, abort, make_response, request
from pandas import DataFrame

from src.utils.mvt import test__get_max_sharpe
from src.utils.data import get_company_data
from src.utils.mvt.compute import compute__max_sharpe

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/")
def root():
    return "<p>APIs on /api route<p>"

@app.route("/api")
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
    _url_params = request.args.get('companies', '')
    try:
        _data = get_company_data(company_names=_url_params.split(','), to_json=True)
    except FileNotFoundError:
        _err_str = 'Request does not have correct company names'
        print(_err_str)
        _resp = make_response({
            "status": "error",
            "data": _err_str
        }, 400)
        return _resp
    except KeyError:
        _err_str = 'Request\'s body does not have correct fields'
        print(_err_str)
        _resp = make_response({
            "status": "error",
            "data": _err_str
        }, 400)
        return _resp

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
        (_weights, _exp_ret, _vol, _sharpe) = compute__max_sharpe(company_names=_json_data['companies'])

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
    
