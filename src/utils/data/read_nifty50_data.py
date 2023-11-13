from typing import Any, Dict, Hashable, List, Optional, Union
import pandas as pd


def get_company_data(
        company_names: Union[str, List[str]],
        field: Optional[str] = 'Close',
        to_json: Optional[bool] = False) -> Union[pd.DataFrame, Dict[Hashable, Any]]:
    if isinstance(company_names, str):
        try:
            _df = pd.read_csv(
                "data/{}.csv".format(company_names), parse_dates=not to_json, index_col="Date")
            _df = _df.rename(columns={"Close": company_names})
            if to_json:
                return _df[[company_names]].to_dict('index')
            else:
                return _df
        except FileNotFoundError as e:
            print("Invalid company name!")
            raise
    elif company_names and all(isinstance(s, str) for s in company_names):
        _dfs = []
        try:
            for name in company_names:
                _df = pd.read_csv("data/{}.csv".format(name), parse_dates=not to_json, index_col="Date")
                _df = _df.rename(columns={"Close": name})
                _dfs.append(_df[[name]])
            _df = pd.concat(_dfs, axis=1)
            if to_json:
                return _df.to_dict('index')
            else:
                return _df
        except FileNotFoundError as e:
            print("At least one invalid company name!")
            raise
    else:
        print("Invalid parameters to get_company_data")
        return {}
