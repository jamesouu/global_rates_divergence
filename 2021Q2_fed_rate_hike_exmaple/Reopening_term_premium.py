import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# 1. Configure Style
plt.style.use('ggplot')
sns.set_palette("pastel")
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.grid': False,
    'font.size': 12
})

# 2. Load & Prepare Data
def load_data():
    df = pd.read_csv('20210615_Reopening.csv', parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    vix_data = {
        '2021-06-10': -13.45, '2021-06-11': -16.01, '2021-06-14': -11.81,
        '2021-06-15': -8.78, '2021-06-16': -4.81, '2021-06-17': 0.09,
        '2021-06-18': 10.95
    }
    df['VIX'] = pd.Series({pd.to_datetime(k): v for k, v in vix_data.items()})
    return df

df = load_data()

# 3. Term Premium Calculation (Adjusted ACM)
def calculate_term_premium(tenY, twoY, vix):
    slope = tenY - twoY
    risk_premium = 0.55 * slope - 0.25 * (vix / 100)
    expected_path = tenY - risk_premium
    return risk_premium, expected_path

# Apply decomposition
df['US_RP'], df['US_EP'] = calculate_term_premium(df['US10Y'], df['US2Y'], df['VIX'])
df['GER_RP'], df['GER_EP'] = calculate_term_premium(df['German10Y'], df['German2Y'], df['VIX'])

# 4. Extract Event Window
event_date = pd.to_datetime('2021-06-15')
window = 5
ew = df.loc[event_date - pd.Timedelta(days=window) :
            event_date + pd.Timedelta(days=window)].copy()

# 5. Plot Stacked Bars with Correct Colors
fig, ax = plt.subplots(figsize=(14, 8))
width = 0.35
x = np.arange(len(ew))
xg = x + width

# Define colors
cols = {
    'US_RP':  '#1F4E79',  # dark blue
    'US_EP':  '#A7C7E7',  # light blue
    'GER_EP': '#B2D7D2',  # mint green
    'GER_RP': '#006F42'   # dark green
}

# Plot US: RP from 0, then EP on top
ax.bar(x, ew['US_RP'], width, bottom=0,
       label='US Risk Premium', color=cols['US_RP'], alpha=0.9)
ax.bar(x, ew['US_EP'], width, bottom=ew['US_RP'],
       label='US Expected Path', color=cols['US_EP'], alpha=0.7)

# Plot Germany: EP from 0, then RP on top
ax.bar(xg, ew['GER_EP'], width, bottom=0,
       label='Germany Expected Path', color=cols['GER_EP'], alpha=0.7)
ax.bar(xg, ew['GER_RP'], width, bottom=0,
       label='Germany Risk Premium', color=cols['GER_RP'], alpha=0.9)

# 6. Customize
ax.set_xticks(x + width/2)
ax.set_xticklabels([d.strftime('%m-%d') for d in ew.index])
ax.set_title(
    'Term Premium Decomposition: Risk Premium vs Expected Path\n'
    '(Post-COVID Reopening Shift, June 10–18, 2021)',
    fontsize=16, pad=15
)
ax.set_ylabel('Term Premium (%)', fontsize=12)
ax.set_facecolor('white')

# Reorder legend: put Germany Risk Premium above Germany Expected Path
handles, labels = ax.get_legend_handles_labels()
order = [
    'US Risk Premium',
    'US Expected Path',
    'Germany Risk Premium',
    'Germany Expected Path'
]
ordered_handles = [handles[labels.index(lbl)] for lbl in order if lbl in labels]
ax.legend(
    ordered_handles,
    order,
    frameon=False,
    bbox_to_anchor=(0.5, -0.1),
    loc='upper center'
)

plt.tight_layout()
plt.show()

# 7. Print DataFrame for Reference
print("=== Term Premium, Risk Premium, Expected Path ===")
print(ew[['US_RP', 'US_EP', 'GER_RP', 'GER_EP']])


