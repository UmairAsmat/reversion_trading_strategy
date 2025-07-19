import pandas as pd
import numpy as np
import yfinance as yf

# Load strategy results
strategy = pd.read_csv('data/djia_strategy_capital.csv', index_col=0, parse_dates=True)
strategy_returns = strategy['Capital'].pct_change().dropna()

# Get start and end dates
start_date = strategy.index[0]
end_date = strategy.index[-1]
if not isinstance(start_date, pd.Timestamp):
    start_date = pd.to_datetime(start_date)
if not isinstance(end_date, pd.Timestamp):
    end_date = pd.to_datetime(end_date)

# Fetch DIA data
dia = yf.download('DIA', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)
if dia is None or dia.empty:
    raise ValueError("DIA data could not be fetched from Yahoo Finance.")
if 'Close' in dia.columns:
    dia = dia[['Close']].copy().rename(columns={'Close': 'DIA'})
elif 'Adj Close' in dia.columns:
    dia = dia[['Adj Close']].copy().rename(columns={'Adj Close': 'DIA'})
else:
    raise ValueError("No 'Close' or 'Adj Close' in DIA data")
dia_returns = dia['DIA'].pct_change().dropna()

# Align dates
common_dates = strategy_returns.index.intersection(dia_returns.index)
strategy_returns = strategy_returns.loc[common_dates]
dia_returns = dia_returns.loc[common_dates]

# Sharpe ratios (rf=0)
strategy_sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
dia_sharpe = dia_returns.mean() / dia_returns.std() * np.sqrt(252)

# Ensure dia_sharpe is a float
if isinstance(dia_sharpe, pd.Series):
    print('Debug: dia_sharpe is a Series, values:', dia_sharpe.values)
    dia_sharpe = dia_sharpe.iloc[0]

print(f"Strategy Sharpe ratio: {strategy_sharpe:.2f}")
print(f"DIA Sharpe ratio: {dia_sharpe:.2f}")

if strategy_sharpe > dia_sharpe:
    print("Our mean reversion strategy outperformed DIA (the Dow Jones ETF) on a risk-adjusted basis.")
else:
    print("DIA (the Dow Jones ETF) outperformed our mean reversion strategy on a risk-adjusted basis.") 