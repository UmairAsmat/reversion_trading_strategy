import pandas as pd
import os
os.makedirs('data', exist_ok=True)

djia_returns = pd.read_csv('data/djia_daily_returns.csv', index_col=0, parse_dates=True)

# Skip the first day (all NaN)
returns_no_first = djia_returns.iloc[1:]

# For each day, get the 10 lowest return stocks
lowest_10 = returns_no_first.apply(lambda row: row.nsmallest(10).index.tolist(), axis=1)
lowest_10_df = pd.DataFrame({
    'Date': lowest_10.index,
    **{f'Rank_{i+1}': [lst[i] if len(lst) > i else None for lst in lowest_10.tolist()] for i in range(10)}
})
lowest_10_df.set_index('Date', inplace=True)
lowest_10_df.to_csv('data/djia_lowest_10_daily.csv') 