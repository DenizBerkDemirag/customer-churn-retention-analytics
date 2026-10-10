from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / "cleaned_telecom_customer_churn.csv"

df = pd.read_csv(DATA_PATH)
fiber_churned = df[(df['Internet Type'] == 'Fiber Optic') & (df['Is_Churned'] == 1)].copy()

def tag_driver(reason):
    r = str(reason).lower()
    if 'speed' in r or 'network' in r:
        return 'Speed & Network Performance'
    elif 'price' in r or 'offer' in r or 'charges' in r or 'data' in r:
        return 'Pricing, Offers & Data Charges'
    elif 'device' in r:
        return 'Competitor Hardware Superiority'
    elif 'attitude' in r or 'support' in r or 'expertise' in r or 'service' in r:
        return 'Customer Support & Service Attitude'
    else:
        return 'Other / Relocation'

fiber_churned['Driver_Group'] = fiber_churned['Churn Reason'].apply(tag_driver)

driver_summary = fiber_churned.groupby('Driver_Group').agg(
    Churned_Customers=('Customer ID', 'count'),
    Percentage=('Customer ID', lambda x: round(len(x) / len(fiber_churned) * 100, 1))
).sort_values(by='Churned_Customers', ascending=False).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
sns.set_theme(style="whitegrid")

top10 = fiber_churned['Churn Reason'].value_counts().head(10).reset_index()
top10.columns = ['Churn Reason', 'Count']
top10['Pct'] = (top10['Count'] / len(fiber_churned) * 100).round(1)

color_map = [
    '#d62728' if any(w in r.lower() for w in ['offer', 'price', 'data'])
    else ('#1f77b4' if 'device' in r.lower()
    else ('#ff7f0e' if any(w in r.lower() for w in ['speed', 'network'])
    else ('#9467bd' if 'attitude' in r.lower() else '#7f7f7f')))
    for r in top10['Churn Reason']
]

bars = axes[0].barh(top10['Churn Reason'][::-1], top10['Count'][::-1], color=color_map[::-1], edgecolor='black', alpha=0.85)
axes[0].set_title(f'Fiber Optic: Top 10 Churn Reasons (Total {len(fiber_churned):,} Churned)', fontsize=13, fontweight='bold', pad=12)
axes[0].set_xlabel('Churned Customer Count')

for bar, pct in zip(bars, top10['Pct'][::-1]):
    axes[0].text(bar.get_width() + 4, bar.get_y() + bar.get_height() / 2.0, f"{int(bar.get_width())} ({pct}%)", 
                 va='center', fontsize=10, fontweight='bold')

palette_driver = ['#d62728', '#9467bd', '#1f77b4', '#7f7f7f', '#ff7f0e']
bars2 = axes[1].bar(range(len(driver_summary)), driver_summary['Percentage'], color=palette_driver, edgecolor='black', alpha=0.85)
axes[1].set_title('Root Cause Comparison: Speed vs. Price vs. Hardware?', fontsize=13, fontweight='bold', pad=12)
axes[1].set_ylabel('Share in Total Fiber Churn (%)')
axes[1].set_xticks(range(len(driver_summary)))
axes[1].set_xticklabels(driver_summary['Driver_Group'], rotation=25, ha='right', fontsize=10)
axes[1].set_ylim(0, 45)

for bar in bars2:
    axes[1].text(bar.get_x() + bar.get_width() / 2.0, bar.get_height() + 0.8, f"{bar.get_height():.1f}%", 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()