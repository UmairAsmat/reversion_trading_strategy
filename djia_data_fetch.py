import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Load DJIA tickers
dj_constituents = pd.read_csv('data/djia_constituents.csv')
symbols = dj_constituents['Symbol'].tolist()

# Set the starting date for historical data (10 years ago from today)
start_date = (datetime.now() - timedelta(days=365*10)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

# Download all tickers at once for efficiency
df = yf.download(
    tickers=symbols,
    start=start_date,
    end=end_date,
    group_by='ticker',
    auto_adjust=False,
    threads=True
)

# If only one ticker, make columns MultiIndex
if not isinstance(df.columns, pd.MultiIndex):
    df.columns = pd.MultiIndex.from_product([df.columns, [symbols[0]]])

# Stack to long format
long_df = df.stack(level=1).reset_index()
if 'level_1' in long_df.columns:
    long_df = long_df.rename(columns={'level_1': 'Symbol'})

# Ensure all required columns exist
required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Symbol']
for col in required_cols:
    if col not in long_df.columns:
        long_df[col] = pd.NA

# Reorder columns
long_df = long_df[required_cols]

# Sort and clean
long_df = long_df.sort_values(by=['Date', 'Symbol'])
long_df = long_df.dropna(subset=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], how='all')

# Save to CSV
long_df.to_csv('data/djia_prices_cleaned.csv', index=False)
print(f"Saved cleaned long-format data to data/djia_prices_cleaned.csv with columns: {required_cols}") 