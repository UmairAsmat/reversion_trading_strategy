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

# Annualized metrics
def annualized_metrics(returns):
    ann_return = (1 + returns).prod() ** (252 / len(returns)) - 1
    ann_vol = returns.std() * np.sqrt(252)
    if isinstance(ann_return, (pd.Series, np.ndarray)):
        print('Debug: ann_return is not scalar:', ann_return)
        ann_return = ann_return.item() if hasattr(ann_return, 'item') else ann_return.iloc[0]
    if isinstance(ann_vol, (pd.Series, np.ndarray)):
        print('Debug: ann_vol is not scalar:', ann_vol)
        ann_vol = ann_vol.item() if hasattr(ann_vol, 'item') else ann_vol.iloc[0]
    sharpe = ann_return / ann_vol if ann_vol != 0 else np.nan
    if isinstance(sharpe, (pd.Series, np.ndarray)):
        print('Debug: sharpe is not scalar:', sharpe)
        sharpe = sharpe.item() if hasattr(sharpe, 'item') else sharpe.iloc[0]
    return ann_return, ann_vol, sharpe

s_ann_return, s_ann_vol, s_sharpe = annualized_metrics(strategy_returns)
d_ann_return, d_ann_vol, d_sharpe = annualized_metrics(dia_returns)

print("\nPerformance Comparison:")
print(f"{'Metric':<25}{'Mean Reversion':>20}{'DIA ETF':>20}")
print(f"{'Annualized Return':<25}{s_ann_return:>20.2%}{d_ann_return:>20.2%}")
print(f"{'Annualized Volatility':<25}{s_ann_vol:>20.2%}{d_ann_vol:>20.2%}")
print(f"{'Sharpe Ratio':<25}{s_sharpe:>20.2f}{d_sharpe:>20.2f}")

if s_sharpe > d_sharpe:
    print("\nThe mean reversion strategy had the higher risk-adjusted return (Sharpe ratio).")
elif s_sharpe < d_sharpe:
    print("\nDIA ETF had the higher risk-adjusted return (Sharpe ratio).")
else:
    print("\nBoth strategies had the same risk-adjusted return (Sharpe ratio).") 