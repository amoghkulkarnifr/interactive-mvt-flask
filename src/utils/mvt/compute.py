from typing import List, Optional, Union

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import pandas as pd

from src.utils.data import get_company_data

def compute__max_sharpe(company_names: Union[List[str], str]):
  _data = get_company_data(company_names=company_names)

  # Calculate expected returns and sample covariance
  mu = expected_returns.capm_return(_data)
  S = risk_models.sample_cov(_data)

  # Optimize for maximal Sharpe ratio
  ef = EfficientFrontier(mu, S)
  weights = ef.max_sharpe()
  (exp_return, volatility, sharpe_ratio) = ef.portfolio_performance(verbose=True)

  return (weights, exp_return, volatility, sharpe_ratio)

def compute__min_volatility(company_names: Union[List[str], str], returns: Optional[float] = 10.0):
  pass

def compute__max_returns(company_names: Union[List[str], str], volatility: Optional[float] = 10.0):
  pass
