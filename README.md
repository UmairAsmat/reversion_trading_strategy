# DJIA Mean Reversion Backtesting Project

## Overview

This project implements and backtests a mean reversion trading strategy on the Dow Jones Industrial Average (DJIA) constituents. The workflow is fully automated, from data fetching to performance analysis and visualization, allowing users to compare the strategy's results against a passive investment in the DIA ETF (which tracks the DJIA).

## Project Structure

- **main.py**: Orchestrates the entire pipeline by running all scripts in sequence.
- **djia_data_fetch.py**: Downloads 10 years of historical price data for all DJIA constituents using Yahoo Finance, cleans it, and saves it in a long-format CSV.
- **djia_daily_returns.py**: Computes daily returns for each DJIA stock and saves them to a CSV file.
- **djia_lowest_returns.py**: For each trading day, identifies the 10 DJIA stocks with the lowest daily returns and saves the results.
- **djia_trading_simulation.py**: Simulates the mean reversion strategy: each day, invests equally in the 10 lowest-returning DJIA stocks from the previous day, tracks capital over time, and saves the capital history.
- **djia_performance_metrics.py**: Calculates annualized return, annualized volatility, and Sharpe ratio for the strategy.
- **djia_comparison.py**: Compares the Sharpe ratio of the strategy to that of the DIA ETF over the same period.
- **side_by_side_metrics.py**: Provides a side-by-side comparison of annualized return, volatility, and Sharpe ratio for both the strategy and DIA ETF.
- **plotly_visualization.py**: Generates interactive plots comparing the growth of $100,000 invested in the strategy versus the DIA ETF.

## Data Sources

- **Yahoo Finance**: All historical price data is fetched using the `yfinance` Python package.
- **data/djia_constituents.csv**: List of DJIA tickers (required for fetching data).

## Trading Strategy: Mean Reversion on DJIA

1. **Universe**: All current DJIA constituents.
2. **Signal**: Each trading day, select the 10 stocks with the lowest daily return from the previous day.
3. **Execution**: Equally allocate capital among these 10 stocks at the next day's open (or close, depending on data granularity).
4. **Rebalancing**: Repeat the process daily, always holding the 10 lowest-returning stocks from the prior day.
5. **Tracking**: Capital is updated based on the performance of the selected stocks, and the process is repeated for the entire backtest period.

## Workflow

1. **Data Fetching**: `djia_data_fetch.py` downloads and cleans historical price data for all DJIA stocks.
2. **Return Calculation**: `djia_daily_returns.py` computes daily returns for each stock.
3. **Stock Selection**: `djia_lowest_returns.py` identifies the 10 lowest-returning stocks each day.
4. **Backtest Simulation**: `djia_trading_simulation.py` simulates the mean reversion strategy, tracking capital over time.
5. **Performance Metrics**: `djia_performance_metrics.py` calculates key metrics (annualized return, volatility, Sharpe ratio).
6. **Benchmark Comparison**: `djia_comparison.py` and `side_by_side_metrics.py` compare the strategy to the DIA ETF.
7. **Visualization**: `plotly_visualization.py` creates interactive plots for visual analysis.

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies:
  - pandas
  - numpy
  - yfinance
  - plotly
  - beautifulsoup4
  - requests

## How to Run

1. Ensure you have all dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Place a valid `djia_constituents.csv` file in the `data/` directory.
3. Run the main pipeline:
   ```bash
   python main.py
   ```
4. Results, metrics, and plots will be saved in the `data/` and `results/` directories.

## Output Files

- `data/djia_prices_cleaned.csv`: Cleaned historical price data for all DJIA stocks.
- `data/djia_daily_returns.csv`: Daily returns for each DJIA stock.
- `data/djia_lowest_10_daily.csv`: Daily list of the 10 lowest-returning stocks.
- `data/djia_strategy_capital.csv`: Capital history of the mean reversion strategy.
- `results/`: Contains interactive plots and visualizations.

## Performance Metrics

- **Annualized Return**: Compound annual growth rate of the strategy.
- **Annualized Volatility**: Standard deviation of daily returns, annualized.
- **Sharpe Ratio**: Risk-adjusted return (assuming risk-free rate = 0).
- **Benchmark Comparison**: All metrics are compared to the DIA ETF.

## Notes

- The strategy is for educational and research purposes only. It does not account for transaction costs, slippage, or survivorship bias.
- Data is sourced from Yahoo Finance via the `yfinance` package.
- The project is modular; each script can be run independently for debugging or analysis.

## License

This project is open source and available under the MIT License. 