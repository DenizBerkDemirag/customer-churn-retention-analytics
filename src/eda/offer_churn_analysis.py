from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / "cleaned_telecom_customer_churn.csv"

df = pd.read_csv(DATA_PATH)

offer_summary = df.groupby('Offer').agg(
    Total_Customers=('Customer ID', 'count'),
    Churn_Count=('Is_Churned', 'sum'),
    Churn_Rate=('Is_Churned', lambda x: round(x.mean() * 100, 2)),
    Total_Lost_Revenue=('Total Revenue', lambda x: round(x[df.loc[x.index, 'Is_Churned'] == 1].sum(), 2))
).reset_index().sort_values(by='Churn_Rate', ascending=False)

contingency_table = pd.crosstab(df['Offer'], df['Customer Status'])
chi2, p_val, dof, _ = chi2_contingency(contingency_table)
print(f"Chi2: {chi2:.4f}, p-value: {p_val:.4e}")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.set_theme(style="whitegrid")

palette_offer = ['#d9534f' if x > 30 else ('#f0ad4e' if x > 20 else '#5cb85c') for x in offer_summary['Churn_Rate']]
bars1 = axes[0].bar(offer_summary['Offer'], offer_summary['Churn_Rate'], 
                    color=palette_offer, edgecolor='black', alpha=0.85, width=0.55)

axes[0].set_title('Churn Rate by Marketing Offer (%)\n(From Highest Risk to Top Retention)', fontsize=13, fontweight='bold', pad=14)
axes[0].set_ylabel('Churn Rate (%)', fontsize=11)
axes[0].set_xlabel('Marketing Offer', fontsize=11)
axes[0].set_ylim(0, 65)

for bar in bars1:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width() / 2.0, yval + 1.2, f'{yval:.1f}%', 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

axes[0].annotate('Highest Risk Campaign:\nOver 50% Churn Rate!', 
                 xy=(0, 52.9), xytext=(0.5, 58),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#c9302c')

axes[0].annotate('Gold Standard (Offer A):\nOnly 6.7% Churn', 
                 xy=(5, 6.7), xytext=(4.0, 18),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#2b7b2b')

ax2_twin = axes[1].twinx()

sns.barplot(data=offer_summary, x='Offer', y='Total_Customers', hue='Offer',
            palette='Blues_d', legend=False, ax=axes[1], alpha=0.8, edgecolor='black')
axes[1].set_title('Campaign Portfolio Volume vs. Lost Revenue ($)', fontsize=13, fontweight='bold', pad=14)
axes[1].set_xlabel('Marketing Offer', fontsize=11)
axes[1].set_ylabel('Total Customer Count', fontsize=11, color='#1f77b4')
axes[1].grid(False)

for p in axes[1].patches:
    axes[1].annotate(f"{int(p.get_height()):,}", 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', 
                     fontweight='bold', fontsize=9)

ax2_twin.plot(range(len(offer_summary)), offer_summary['Total_Lost_Revenue'] / 1e6, 
              color='#d9534f', marker='s', linewidth=2.5, markersize=8)
ax2_twin.set_ylabel('Total Lost Revenue ($ Millions)', fontsize=11, color='#d9534f')
ax2_twin.set_ylim(0, 2.5)
ax2_twin.grid(True, linestyle=':', alpha=0.5)

for i, y in enumerate(offer_summary['Total_Lost_Revenue'] / 1e6):
    ax2_twin.annotate(f"${y:.2f}M", (i, y), textcoords="offset points", xytext=(0, 8), 
                      ha='center', fontsize=10, fontweight='bold', color='#d9534f')

plt.tight_layout()
plt.show()