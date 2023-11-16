from typing import List, Optional, Union

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import pandas as pd

from src.utils.data import get_company_data

def __get_efficient_frontier(_data: pd.DataFrame):
  # Calculate expected returns and sample covariance
  mu = expected_returns.ema_historical_return(_data)
  S = risk_models.sample_cov(_data)

  # Optimize for maximal Sharpe ratio
  ef = EfficientFrontier(mu, S)

  return ef

def compute__max_sharpe(company_names: Union[List[str], str]):
  _data = get_company_data(company_names=company_names)
  weights = exp_return = volatility = sharpe_ratio = None

  # Should alwas return True
  if isinstance(_data, pd.DataFrame):
    ef = __get_efficient_frontier(_data)
    weights = ef.max_sharpe()
    (exp_return, volatility, sharpe_ratio) = ef.portfolio_performance()

  return (weights, exp_return, volatility, sharpe_ratio)

def compute__min_volatility(company_names: Union[List[str], str], returns: Optional[float] = 10.0):
  _data = get_company_data(company_names=company_names)
  weights = exp_return = volatility = sharpe_ratio = None

  # Should alwas return True
  if isinstance(_data, pd.DataFrame):
    ef = __get_efficient_frontier(_data)
    weights = ef.min_volatility()
    (exp_return, volatility, sharpe_ratio) = ef.portfolio_performance()

  return (weights, exp_return, volatility, sharpe_ratio)

def compute__custom(company_names: Union[List[str], str], weights: List[float]):
  _data = get_company_data(company_names=company_names)
  exp_return = volatility = sharpe_ratio = None

  if isinstance(_data, pd.DataFrame):
    ef = __get_efficient_frontier(_data)
    # Call ef.set_weights()

  # 
  return (weights, exp_return, volatility, sharpe_ratio)
