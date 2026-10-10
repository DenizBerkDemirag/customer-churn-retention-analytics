from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / "cleaned_telecom_customer_churn.csv"

df = pd.read_csv(DATA_PATH)

internet_df = df[df['Internet Service'] == 'Yes'].copy()
addon_summary = internet_df.groupby('Total_Addon_Services').agg(
    Total_Customers=('Customer ID', 'count'),
    Churn_Rate=('Is_Churned', lambda x: round(x.mean() * 100, 1))
).reset_index()

def categorize_service_depth(row):
    if row['Internet Service'] == 'No':
        return '1. No Internet Service\n(Landline Only)'
    elif row['Total_Addon_Services'] == 0:
        return '2. Solo Internet\n(0 Add-ons)'
    elif row['Total_Addon_Services'] <= 3:
        return '3. Low Integration\n(1-3 Add-ons)'
    else:
        return '4. Full Ecosystem\n(4-7 Add-ons)'

df['Service_Depth'] = df.apply(categorize_service_depth, axis=1)

depth_order = [
    '1. No Internet Service\n(Landline Only)',
    '2. Solo Internet\n(0 Add-ons)',
    '3. Low Integration\n(1-3 Add-ons)',
    '4. Full Ecosystem\n(4-7 Add-ons)'
]
depth_summary = df.groupby('Service_Depth').agg(
    Total_Customers=('Customer ID', 'count'),
    Churn_Rate=('Is_Churned', lambda x: round(x.mean() * 100, 1))
).reindex(depth_order).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.set_theme(style="whitegrid")

colors_p1 = ['#d9534f' if x == 0 else ('#f0ad4e' if x <= 3 else '#5cb85c') for x in addon_summary['Total_Addon_Services']]
bars1 = axes[0].bar(addon_summary['Total_Addon_Services'], addon_summary['Churn_Rate'], 
                     color=colors_p1, width=0.65, edgecolor='black', alpha=0.85)

axes[0].set_title(f'Churn Rate by Number of Add-on Services (%)\n(Internet Users - {len(internet_df):,} Customers)', fontsize=13, fontweight='bold', pad=14)
axes[0].set_xlabel('Number of Value-Added Services (Security, Backup, TV, etc.)', fontsize=11)
axes[0].set_ylabel('Churn Rate (%)', fontsize=11)
axes[0].set_xticks(range(0, 8))
axes[0].set_ylim(0, 60)

for bar in bars1:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width() / 2.0, yval + 1.2, f'{yval:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

axes[0].annotate('Solo Internet Users:\nHalf of them leave!', 
                 xy=(0, 50.4), xytext=(0.8, 54),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#c9302c')

colors_p2 = ['#777777', '#d9534f', '#f0ad4e', '#5cb85c']
bars2 = axes[1].bar(range(len(depth_summary)), depth_summary['Churn_Rate'], 
                     color=colors_p2, width=0.55, edgecolor='black', alpha=0.85)

axes[1].set_title(f'Service Depth Segments vs. Churn Rate\n(Full Portfolio - {len(df):,} Customers)', fontsize=13, fontweight='bold', pad=14)
axes[1].set_xlabel('Customer Service Segment', fontsize=11)
axes[1].set_ylabel('Churn Rate (%)', fontsize=11)
axes[1].set_xticks(range(len(depth_summary)))
axes[1].set_xticklabels(depth_summary['Service_Depth'], fontsize=10)
axes[1].set_ylim(0, 60)

for bar in bars2:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width() / 2.0, yval + 1.2, f'{yval:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

for bar, total in zip(bars2, depth_summary['Total_Customers']):
    axes[1].text(bar.get_x() + bar.get_width() / 2.0, 4, f'N={total:,}', ha='center', va='bottom', fontsize=9, color='white', fontweight='bold')

plt.tight_layout()
plt.show()