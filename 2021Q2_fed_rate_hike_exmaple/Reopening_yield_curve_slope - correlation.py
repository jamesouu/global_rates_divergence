import pandas as pd

# Load the data from the CSV file
file_path = '20210615_Reopening.csv'  # Provide the correct file path
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set the Date as the index
df.set_index('Date', inplace=True)

# Define the event window (5 days before and after the event)
event_date = pd.to_datetime('2021-06-15')
event_window_start = event_date - pd.Timedelta(days=5)
event_window_end = event_date + pd.Timedelta(days=5)

# Filter the data for the event window (without extending the date range)
event_window_data = df.loc[event_window_start:event_window_end]

# Calculate Yield Curve Slopes for each day in the event window
event_window_data['US_Yield_Curve_slope'] = event_window_data['US10Y'] - event_window_data['US2Y']
event_window_data['German_Yield_Curve_slope'] = event_window_data['German10Y'] - event_window_data['German2Y']

# Calculate correlation between US 10Y and German 10Y yields
correlation_us_german_10y = event_window_data[['US10Y', 'German10Y']].corr().iloc[0, 1]

# Calculate correlation between US 2Y and German 2Y yields
correlation_us_german_2y = event_window_data[['US2Y', 'German2Y']].corr().iloc[0, 1]

# Output results for each day in the event window
print(f"Yield Curve Slopes from {event_window_start.date()} to {event_window_end.date()}:")
for date, row in event_window_data.iterrows():
    print(f"{date.date()} - US Yield Curve Slope: {row['US_Yield_Curve_slope']:.2f}, "
          f"German Yield Curve Slope: {row['German_Yield_Curve_slope']:.2f}")

# Print correlation results
print(f"\nCorrelation between US 10Y and German 10Y yields: {correlation_us_german_10y:.2f}")
print(f"Correlation between US 2Y and German 2Y yields: {correlation_us_german_2y:.2f}")