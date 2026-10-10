from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.proportion import proportions_ztest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / "cleaned_telecom_customer_churn.csv"

# 1. Load and filter dataset
df = pd.read_csv(DATA_PATH)
pay_df = df[df['Payment Method'].isin(['Bank Withdrawal', 'Credit Card'])].copy()

# 2. Summary Metrics
pay_summary = pay_df.groupby('Payment Method').agg(
    Total_Customers=('Customer ID', 'count'),
    Churn_Count=('Is_Churned', 'sum'),
    Churn_Rate=('Is_Churned', lambda x: round(x.mean() * 100, 2))
).reset_index()

# 3. Two-proportion Z-Test
count = pay_summary['Churn_Count'].values
nobs = pay_summary['Total_Customers'].values
z_stat, p_val = proportions_ztest(count, nobs)
print(f"Z-Stat: {z_stat:.4f}, p-value: {p_val:.4e}")

# 4. Visualization (2 Panels)
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
sns.set_theme(style="whitegrid")

# Panel 1: Overall Comparison
bars1 = axes[0].bar(pay_summary['Payment Method'], pay_summary['Churn_Rate'], 
                    color=['#d9534f', '#5cb85c'], edgecolor='black', alpha=0.85, width=0.5)
axes[0].set_title('Churn Rate by Payment Method (%)\n(Bank Withdrawal vs. Credit Card)', fontsize=13, fontweight='bold', pad=14)
axes[0].set_ylabel('Churn Rate (%)', fontsize=11)
axes[0].set_ylim(0, 45)

for bar in bars1:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width() / 2.0, yval + 1.0, f'{yval:.2f}%', 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

axes[0].annotate('2.35x Higher Risk!\n(p < 0.001)', 
                 xy=(0, 34.0), xytext=(0.3, 38),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#c9302c')

# Panel 2: Breakdown by Contract Type
contract_order = ['Month-to-Month', 'One Year', 'Two Year']
c_df = pay_df.groupby(['Payment Method', 'Contract'], observed=False)['Is_Churned'].mean().reset_index()
c_df['Churn_Rate'] = c_df['Is_Churned'] * 100

sns.barplot(data=c_df, x='Contract', y='Churn_Rate', hue='Payment Method', 
            palette=['#d9534f', '#5cb85c'], ax=axes[1], order=contract_order, edgecolor='black', alpha=0.85)
axes[1].set_title('Churn Rate by Payment Method Across Contract Types (%)', fontsize=13, fontweight='bold', pad=14)
axes[1].set_ylabel('Churn Rate (%)', fontsize=11)
axes[1].set_xlabel('Contract Type', fontsize=11)
axes[1].set_ylim(0, 60)
axes[1].legend(title='Payment Method', loc='upper right')

for p in axes[1].patches:
    h = p.get_height()
    if h > 0:
        axes[1].annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h), 
                         ha='center', va='bottom', xytext=(0, 4), textcoords='offset points', 
                         fontweight='bold', fontsize=10)

plt.tight_layout()
plt.show()