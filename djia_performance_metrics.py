import pandas as pd
import numpy as np

results = pd.read_csv('data/djia_strategy_capital.csv', index_col=0, parse_dates=True)
capital = results['Capital']

# Daily returns
returns = capital.pct_change().dropna()

# Annualized return
start_date = capital.index[0]
end_date = capital.index[-1]
if not isinstance(start_date, pd.Timestamp):
    start_date = pd.to_datetime(start_date)
if not isinstance(end_date, pd.Timestamp):
    end_date = pd.to_datetime(end_date)
num_years = (end_date - start_date).days / 365.25
annualized_return = (capital.iloc[-1] / capital.iloc[0]) ** (1/num_years) - 1

# Annualized volatility
annualized_vol = returns.std() * np.sqrt(252)

# Sharpe ratio (rf=0)
sharpe = annualized_return / annualized_vol if annualized_vol != 0 else np.nan

print(f"Annualized return: {annualized_return:.2%}")
print(f"Annualized volatility: {annualized_vol:.2%}")
print(f"Sharpe ratio: {sharpe:.2f}") 