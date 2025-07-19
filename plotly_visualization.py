import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
import os
os.makedirs('results', exist_ok=True)

# Load strategy results
strategy = pd.read_csv('data/djia_strategy_capital.csv', index_col=0, parse_dates=True)
strategy_returns = strategy['Capital'].pct_change().fillna(0)

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
dia = dia.reindex(strategy.index).ffill()
dia_returns = dia['DIA'].pct_change().fillna(0)

# Cumulative returns
strategy_cum = (1 + strategy_returns).cumprod()
dia_cum = (1 + dia_returns).cumprod()

initial_investment = 100_000
strategy_portfolio = strategy_cum * initial_investment
# For DIA, align to same initial investment
if not np.isclose(dia_cum.iloc[0], 1.0):
    dia_cum = dia_cum / dia_cum.iloc[0]
dia_portfolio = dia_cum * initial_investment

# Plotly interactive plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=strategy.index, y=strategy_portfolio, mode='lines', name='Mean Reversion Strategy'))
fig.add_trace(go.Scatter(x=strategy.index, y=dia_portfolio, mode='lines', name='DIA ETF'))
fig.update_layout(
    title='Growth of $100,000 Portfolio: Mean Reversion Strategy vs DIA ETF',
    xaxis_title='Date',
    yaxis_title='Portfolio Value (USD)',
    legend_title='Strategy',
    hovermode='x unified',
    template='plotly_white'
)

# Save as static PNG (requires kaleido)
fig.write_image("results/djia_vs_dia.png")
print("Plot saved as results/djia_vs_dia.png (static image)")

# Save as interactive HTML
fig.write_html("results/djia_vs_dia.html")
print("Interactive plot saved as results/djia_vs_dia.html") 