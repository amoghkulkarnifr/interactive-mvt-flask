from flask import Flask, abort, make_response, request
from pandas import DataFrame

from src.utils.mvt import test__get_max_sharpe
from src.utils.data import get_company_data
from src.utils.mvt.compute import compute__custom, compute__max_sharpe

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def __get_error_response_obj(resp_code: int, error_msg: str, debug: bool=True):
    print(error_msg)
    return make_response({
        "status": "error",
        "data": error_msg
    }, resp_code)

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
        return __get_error_response_obj(
            error_msg='Request does not have correct company names', 
            resp_code=400)
    except KeyError:
        return __get_error_response_obj(
            error_msg='Request\'s body does not have correct fields', 
            resp_code=400)
    except:
        return __get_error_response_obj(
            error_msg='Server error', 
            resp_code=400)

    return {
        "status": "OK",
        "data": _data
    }

@app.route("/api/compute", methods=['POST'])
def api_compute():
    _json_data = request.get_json()
    
    try:
        opt_portfolio = request.args.get('optPortfolio', '', type=str)
    except KeyError as e:
        return __get_error_response_obj(
            error_msg='Invalid/absent url parameters', 
            resp_code=400)
    
    if opt_portfolio == "maxSharpeRatio":
        try:
            (_weights, _exp_ret, _vol, _sharpe) = compute__max_sharpe(company_names=_json_data['companies'])
        except KeyError as e:
            return __get_error_response_obj(
                error_msg='Invalid data in the request body', 
                resp_code=400)

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
    elif opt_portfolio == "custom":
        try:
            (_weights, _exp_ret, _vol, _sharpe) = compute__custom(
                company_names=_json_data['companies'],
                weights=_json_data['weights'])
        except KeyError as e:
            return __get_error_response_obj(
                error_msg='Invalid/absent url parameters', 
                resp_code=400)
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
        return __get_error_response_obj(
            error_msg='Invalid parameter values',
            resp_code=400)
    
