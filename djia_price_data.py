import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Initialize an empty dataframe for storing stock data
stock_data = pd.DataFrame()
dj_constituents = pd.read_csv('data/djia_constituents.csv')
# Set the starting date for historical data (10 years ago from today)
start_date = datetime.now() - timedelta(days=365*10)

for symbol in dj_constituents['Symbol']:
    try:
        ticker_data = yf.download(symbol, start=start_date)
        ticker_data['Symbol'] = symbol
        stock_data = pd.concat([stock_data, ticker_data])
    except Exception as e:
        print(f"Error occurred for symbol: {symbol}, {str(e)}")

# Save the fetched data to CSV
stock_data.to_csv('data/dow_jones_data.csv')

# Load the data from CSV to pandas DataFrame
dj_constituents = pd.read_csv('data/dow_jones_constituents.csv')
dj_data = pd.read_csv('data/djia_prices_cleaned.csv')

# Replace missing data using forward fill method
dj_constituents.fillna(method='ffill', inplace=True)
dj_data.fillna(method='ffill', inplace=True)