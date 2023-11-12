from logging import error
from typing import List, Optional, Union
import pandas as pd

def get_company_data(company_names: Union[str, List[str]], field: Optional[str] = 'Close'):
  if isinstance(company_names, str):
    try:
      _df = pd.read_csv("data/{}.csv".format(company_names), index_col="Date")
      _df = _df.rename(columns={"Close": company_names})
      return _df[[company_names]].to_dict('index')
    except FileNotFoundError as e:
      print("Invalid company name!")
      raise
  elif company_names and all(isinstance(s, str) for s in company_names):
    _dfs = []
    try:
      for name in company_names:
        _df = pd.read_csv("data/{}.csv".format(name), index_col="Date")
        _df = _df.rename(columns={"Close": name})
        _dfs.append(_df[[name]])
      _df = pd.concat(_dfs, axis=1)
      return _df.to_dict('index')
    except FileNotFoundError as e:
      print("Invalid company name!")
      raise
