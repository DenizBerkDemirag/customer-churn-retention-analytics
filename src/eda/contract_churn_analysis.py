from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / "cleaned_telecom_customer_churn.csv"

df = pd.read_csv(DATA_PATH)

contract_order = ['Month-to-Month', 'One Year', 'Two Year']
df['Contract'] = pd.Categorical(df['Contract'], categories=contract_order, ordered=True)

contract_summary = df.groupby('Contract', observed=False).agg(
    Total_Customers=('Customer ID', 'count'),
    Churn_Count=('Is_Churned', 'sum'),
    Churn_Rate=('Is_Churned', lambda x: round(x.mean() * 100, 2)),
    Total_Lost_Revenue=('Total Revenue', lambda x: round(x[df.loc[x.index, 'Is_Churned'] == 1].sum(), 2))
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.set_theme(style="whitegrid")

palette_contract = ['#d9534f', '#f0ad4e', '#5cb85c']
bars1 = axes[0].bar(contract_summary['Contract'], contract_summary['Churn_Rate'], 
                    color=palette_contract, edgecolor='black', alpha=0.85, width=0.5)

axes[0].set_title('Churn Rate by Contract Type (%)\n(Month-to-Month vs. Long-Term Contracts)', fontsize=13, fontweight='bold', pad=14)
axes[0].set_ylabel('Churn Rate (%)', fontsize=11)
axes[0].set_xlabel('Contract Type', fontsize=11)
axes[0].set_ylim(0, 55)

for bar in bars1:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width() / 2.0, yval + 1.2, f'{yval:.2f}%', 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

axes[0].annotate('18x Risk Difference!\n(Month-to-Month: 45.8% vs 2-Year: 2.5%)', 
                 xy=(0, 45.84), xytext=(0.4, 49),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#c9302c')

ax2_twin = axes[1].twinx()

sns.barplot(data=contract_summary, x='Contract', y='Churn_Count', hue='Contract',
            palette='Reds_d', legend=False, ax=axes[1], alpha=0.85, edgecolor='black')
axes[1].set_title('Lost Customers vs. Lost Revenue ($) by Contract', fontsize=13, fontweight='bold', pad=14)
axes[1].set_xlabel('Contract Type', fontsize=11)
axes[1].set_ylabel('Churned Customers (Count)', fontsize=11, color='#b22222')
axes[1].set_ylim(0, 2000)
axes[1].grid(False)

for p in axes[1].patches:
    axes[1].annotate(f"{int(p.get_height()):,} Customers", 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', 
                     fontweight='bold', fontsize=10)

ax2_twin.plot(range(len(contract_summary)), contract_summary['Total_Lost_Revenue'] / 1e6, 
              color='#1f77b4', marker='s', linewidth=2.5, markersize=8)
ax2_twin.set_ylabel('Total Lost Revenue ($ Millions)', fontsize=11, color='#1f77b4')
ax2_twin.set_ylim(0, 3.2)
ax2_twin.grid(True, linestyle=':', alpha=0.5)

for i, y in enumerate(contract_summary['Total_Lost_Revenue'] / 1e6):
    ax2_twin.annotate(f"${y:.2f}M", (i, y), textcoords="offset points", xytext=(0, 8), 
                      ha='center', fontsize=10, fontweight='bold', color='#1f77b4')

plt.tight_layout()
plt.show()