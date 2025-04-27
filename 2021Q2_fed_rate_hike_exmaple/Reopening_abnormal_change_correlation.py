import pandas as pd

# Load the data from the CSV file
file_path = '20210615_Reopening.csv'  # Provide the correct file path
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set the Date as the index
df.set_index('Date', inplace=True)

# Define the event window (5 days before and after the election)
event_date = pd.to_datetime('2021-06-15')
event_window_start = event_date - pd.Timedelta(days=5)
event_window_end = event_date + pd.Timedelta(days=5)

# Filter the data for the event window (without extending the date range)
event_window_data = df.loc[event_window_start:event_window_end].copy()  # Use .copy() to avoid the SettingWithCopyWarning

# Calculate abnormal yield changes (daily differences) for each bond
event_window_data['US10Y_change'] = event_window_data['US10Y'].diff()
event_window_data['US2Y_change'] = event_window_data['US2Y'].diff()
event_window_data['German10Y_change'] = event_window_data['German10Y'].diff()
event_window_data['German2Y_change'] = event_window_data['German2Y'].diff()

# Calculate the correlation between abnormal yield changes for U.S. and German bonds
correlation_us_german_10y = event_window_data[['US10Y_change', 'German10Y_change']].corr().iloc[0, 1]
correlation_us_german_2y = event_window_data[['US2Y_change', 'German2Y_change']].corr().iloc[0, 1]

# Output results
print(f"Correlation between US 10Y and German 10Y abnormal yield changes: {correlation_us_german_10y}")
print(f"Correlation between US 2Y and German 2Y abnormal yield changes: {correlation_us_german_2y}")