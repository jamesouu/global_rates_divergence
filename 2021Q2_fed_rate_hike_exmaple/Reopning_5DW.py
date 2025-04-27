import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = '20210615_Reopening.csv'  # Provide the correct file path
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set the Date as the index
df.set_index('Date', inplace=True)

# Define the event date and event window
event_date = pd.to_datetime('2021-06-15')
event_window_start = event_date - pd.Timedelta(days=5)
event_window_end = event_date + pd.Timedelta(days=5)

# Filter the data for the event window (without extending the date range)
event_window_data = df.loc[event_window_start:event_window_end]

# Calculate the 5-day average yield for both 10Y and 2Y for US and Germany (before the event)
pre_event_data = df.loc[event_window_start:event_date - pd.Timedelta(days=1)]
us_10y_avg_pre_event = pre_event_data['US10Y'].mean()
us_2y_avg_pre_event = pre_event_data['US2Y'].mean()
german_10y_avg_pre_event = pre_event_data['German10Y'].mean()
german_2y_avg_pre_event = pre_event_data['German2Y'].mean()

# Calculate the abnormal yield changes by subtracting the pre-event average
event_window_data['US10Y_abnormal_change'] = event_window_data['US10Y'] - us_10y_avg_pre_event
event_window_data['US2Y_abnormal_change'] = event_window_data['US2Y'] - us_2y_avg_pre_event
event_window_data['German10Y_abnormal_change'] = event_window_data['German10Y'] - german_10y_avg_pre_event
event_window_data['German2Y_abnormal_change'] = event_window_data['German2Y'] - german_2y_avg_pre_event

# Calculate the yield curve change (10Y - 2Y) for both US and Germany
event_window_data['US_Yield_Curve_change'] = event_window_data['US10Y_abnormal_change'] - event_window_data['US2Y_abnormal_change']
event_window_data['German_Yield_Curve_change'] = event_window_data['German10Y_abnormal_change'] - event_window_data['German2Y_abnormal_change']

# Plotting the line chart and stacked bar chart
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot US 10Y and 2Y abnormal yield changes on the left y-axis, set zorder to bring it to the front
ax1.plot(event_window_data.index, event_window_data['US10Y_abnormal_change'], label='US 10Y Abnormal Change', color='darkblue', marker='o', linestyle='-', linewidth=2, zorder=3)
ax1.plot(event_window_data.index, event_window_data['US2Y_abnormal_change'], label='US 2Y Abnormal Change', color='lightblue', marker='o', linestyle='--', linewidth=2, zorder=3)
ax1.plot(event_window_data.index, event_window_data['German10Y_abnormal_change'], label='German 10Y Abnormal Change', color='darkgreen', marker='o', linestyle='-', linewidth=2, zorder=3)
ax1.plot(event_window_data.index, event_window_data['German2Y_abnormal_change'], label='German 2Y Abnormal Change', color='lightgreen', marker='o', linestyle='--', linewidth=2, zorder=3)

# Customize the left y-axis
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Daily Abnormal Yield Change (%)', fontsize=12)
ax1.set_title('Daily Abnormal Yield Changes & Yield Curve Changes Around the 2021 Reopening Early Stage', fontsize=14)
ax1.grid(False)

# Create a second y-axis to plot the stacked bar chart for the yield curve changes
ax2 = ax1.twinx()

# Plot the stacked bar chart for yield curve changes (10Y - 2Y difference) with transparent fill and colored edges
ax2.bar(event_window_data.index, event_window_data['US_Yield_Curve_change'], width=0.4, label='US Yield Curve Change', color='none', edgecolor='darkblue', alpha=0.6, zorder=2)
ax2.bar(event_window_data.index, event_window_data['German_Yield_Curve_change'], width=0.4, label='German Yield Curve Change', color='none', edgecolor='darkgreen', alpha=0.6, bottom=event_window_data['US_Yield_Curve_change'], zorder=2)

# Customize the right y-axis
ax2.set_ylabel('Yield Curve Change (10Y - 2Y)', fontsize=12)

# Combine the legends from both axes and position the legend below the chart
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)

# Final plot adjustments
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()