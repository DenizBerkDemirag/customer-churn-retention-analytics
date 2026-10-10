from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / "cleaned_telecom_customer_churn.csv"

df = pd.read_csv(DATA_PATH)

def combo_group(row):
    sec = row['Online Security']
    tech = row['Premium Tech Support']
    if sec == 'No Internet Service' or tech == 'No Internet Service':
        return 'No Internet\n(Baseline)'
    elif sec == 'Yes' and tech == 'Yes':
        return 'Both Active\n(Full Shield)'
    elif sec == 'Yes' and tech == 'No':
        return 'Security\nOnly'
    elif sec == 'No' and tech == 'Yes':
        return 'Tech Support\nOnly'
    else:
        return 'Neither\n(Unprotected)'

df['Security_Support_Combo'] = df.apply(combo_group, axis=1)

combo_order = [
    'Neither\n(Unprotected)',
    'Security\nOnly',
    'Tech Support\nOnly',
    'Both Active\n(Full Shield)',
    'No Internet\n(Baseline)'
]

combo_stats = df.groupby('Security_Support_Combo').agg(
    Total_Customers=('Customer ID', 'count'),
    Churn_Rate=('Is_Churned', lambda x: round(x.mean() * 100, 1))
).reindex(combo_order).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.set_theme(style="whitegrid")

internet_df = df[df['Internet Service'] == 'Yes'].copy()
sec_comp = internet_df.groupby('Online Security')['Is_Churned'].mean().reset_index()
sec_comp['Service'] = 'Online Security'
tech_comp = internet_df.groupby('Premium Tech Support')['Is_Churned'].mean().reset_index()
tech_comp['Service'] = 'Premium Tech Support'

single_df = pd.concat([
    sec_comp.rename(columns={'Online Security': 'Status'}),
    tech_comp.rename(columns={'Premium Tech Support': 'Status'})
])
single_df['Churn_Rate'] = single_df['Is_Churned'] * 100

sns.barplot(data=single_df, x='Service', y='Churn_Rate', hue='Status', 
            palette=['#d9534f', '#5cb85c'], ax=axes[0], edgecolor='black', alpha=0.85)
axes[0].set_title('Churn Rate by Value-Added Service for Internet Subscribers (%)\n(Active vs Inactive Users)', fontsize=13, fontweight='bold', pad=14)
axes[0].set_ylabel('Churn Rate (%)')
axes[0].set_xlabel('')
axes[0].set_ylim(0, 50)
axes[0].legend(title='Subscription Status', loc='upper right')

for p in axes[0].patches:
    h = p.get_height()
    if h > 0:
        axes[0].annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h), 
                         ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', 
                         fontweight='bold', fontsize=11)

colors_p2 = ['#d9534f', '#f0ad4e', '#f0ad4e', '#5cb85c', '#777777']
bars2 = axes[1].bar(combo_stats['Security_Support_Combo'], combo_stats['Churn_Rate'], 
                    color=colors_p2, edgecolor='black', alpha=0.85, width=0.6)

axes[1].set_title('Synergy Impact of Security & Support Packages (%)\n(Combination Analysis)', fontsize=13, fontweight='bold', pad=14)
axes[1].set_ylabel('Churn Rate (%)')
axes[1].set_xlabel('')
axes[1].set_ylim(0, 60)

for bar in bars2:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width() / 2.0, yval + 1.2, f'{yval:.1f}%', 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

axes[1].annotate('Highest Churn Risk:\nOver 49% Churn Rate', 
                 xy=(0, 49.0), xytext=(0.4, 53),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#c9302c')

plt.tight_layout()
plt.show()