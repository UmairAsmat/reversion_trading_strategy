import pandas as pd
import os
os.makedirs('data', exist_ok=True)

djia_prices = pd.read_csv('data/djia_prices_cleaned.csv', index_col=0, parse_dates=True)

djia_returns = djia_prices.pct_change()

djia_returns.to_csv('data/djia_daily_returns.csv') 