import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

def test__get_max_sharpe():
  # Read in price data
  df = pd.read_csv("src/utils/mvt/stock_prices.csv", parse_dates=True, index_col="date")

  # Calculate expected returns and sample covariance
  mu = expected_returns.mean_historical_return(df)
  S = risk_models.sample_cov(df)

  # Optimize for maximal Sharpe ratio
  ef = EfficientFrontier(mu, S)
  weights = ef.max_sharpe()
  ef.portfolio_performance(verbose=True)

  return weights