import pandas as pd
import numpy as np
import os
os.makedirs('data', exist_ok=True)

# Load data
prices = pd.read_csv('data/djia_prices_cleaned.csv', index_col=0, parse_dates=True)
lowest_10 = pd.read_csv('data/djia_lowest_10_daily.csv', index_col=0, parse_dates=True)

# Debug: print head of data
print('First few rows of prices:')
print(prices.head())
print('First few rows of lowest_10:')
print(lowest_10.head())

if prices.empty or lowest_10.empty:
    print('ERROR: Price or lowest_10 DataFrame is empty. Check data preparation steps.')
    exit(1)
if prices.isnull().all().all():
    print('ERROR: All price data is NaN. Check data fetching and cleaning.')
    exit(1)

# Ensure dates are datetime
prices.index = pd.to_datetime(prices.index)
lowest_10.index = pd.to_datetime(lowest_10.index)

initial_capital = 100_000
capital = initial_capital
capital_history = []
dates = []

for i, date in enumerate(lowest_10.index):
    if i+1 >= len(prices.index):
        break  # No next day
    today = date
    next_day = prices.index[prices.index.get_loc(today) + 1] if today in prices.index and prices.index.get_loc(today) + 1 < len(prices.index) else None
    if next_day is None:
        break
    stocks = lowest_10.loc[today].dropna().values
    if len(stocks) < 10:
        # Not enough stocks, skip
        capital_history.append(capital)
        dates.append(today)
        continue
    # Get today's and next day's prices
    try:
        today_prices = prices.loc[today, stocks]
        next_prices = prices.loc[next_day, stocks]
    except Exception as e:
        # Missing data, skip
        capital_history.append(capital)
        dates.append(today)
        continue
    if today_prices.isnull().any() or next_prices.isnull().any():
        # Skip if any price is missing
        capital_history.append(capital)
        dates.append(today)
        continue
    # Equal allocation
    allocation = capital / 10
    shares = allocation / today_prices
    proceeds = shares * next_prices
    capital = proceeds.sum()
    capital_history.append(capital)
    dates.append(today)

# Store results
results_df = pd.DataFrame({'Date': dates, 'Capital': capital_history})
results_df.set_index('Date', inplace=True)
results_df.to_csv('data/djia_strategy_capital.csv')

print(f"Final capital: ${capital:,.2f}")
total_return = (capital / initial_capital) - 1
print(f"Total return: {total_return:.2%}") 