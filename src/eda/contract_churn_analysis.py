import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

df = pd.read_csv('telecom_customer_churn_clean.csv')

contract_order = ['Month-to-Month', 'One Year', 'Two Year']
df['Contract'] = pd.Categorical(df['Contract'], categories=contract_order, ordered=True)

contract_summary = df.groupby('Contract', observed=False).agg(
    Toplam_Musteri=('Customer ID', 'count'),
    Churn_Sayisi=('Is_Churned', 'sum'),
    Churn_Orani=('Is_Churned', lambda x: round(x.mean() * 100, 2)),
    Toplam_Kayip_Ciro=('Total Revenue', lambda x: round(x[df.loc[x.index, 'Is_Churned'] == 1].sum(), 2))
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.set_theme(style="whitegrid")

palette_contract = ['#d9534f', '#f0ad4e', '#5cb85c']
bars1 = axes[0].bar(contract_summary['Contract'], contract_summary['Churn_Orani'], 
                    color=palette_contract, edgecolor='black', alpha=0.85, width=0.5)

axes[0].set_title('Sözleşme Türüne Göre Churn Oranı (%)\n(Taahhütsüz vs. Taahhütlü)', fontsize=13, fontweight='bold', pad=14)
axes[0].set_ylabel('Churn Oranı (%)', fontsize=11)
axes[0].set_xlabel('Sözleşme Türü (Contract)', fontsize=11)
axes[0].set_ylim(0, 55)

for bar in bars1:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f'%{yval:.2f}', 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

axes[0].annotate('18 Kat Risk Farkı!\n(Aylık: %45.8 vs 2 Yıllık: %2.5)', 
                 xy=(0, 45.84), xytext=(0.4, 49),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#c9302c')

ax2_twin = axes[1].twinx()

sns.barplot(data=contract_summary, x='Contract', y='Churn_Sayisi', 
            palette='Reds_d', ax=axes[1], alpha=0.85, edgecolor='black')
axes[1].set_title('Sözleşme Bazında Kaybedilen Müşteri Sayısı vs. Kayıp Ciro ($)', fontsize=13, fontweight='bold', pad=14)
axes[1].set_xlabel('Sözleşme Türü (Contract)', fontsize=11)
axes[1].set_ylabel('Ayrılan Müşteri Sayısı (Kişi)', fontsize=11, color='#b22222')
axes[1].set_ylim(0, 2000)
axes[1].grid(False)

for p in axes[1].patches:
    axes[1].annotate(f"{int(p.get_height()):,} Kişi", 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', 
                     fontweight='bold', fontsize=10)

ax2_twin.plot(range(len(contract_summary)), contract_summary['Toplam_Kayip_Ciro'] / 1e6, 
              color='#1f77b4', marker='s', linewidth=2.5, markersize=8)
ax2_twin.set_ylabel('Toplam Kayıp Ciro ($ Milyon)', fontsize=11, color='#1f77b4')
ax2_twin.set_ylim(0, 3.2)
ax2_twin.grid(True, linestyle=':', alpha=0.5)

for i, y in enumerate(contract_summary['Toplam_Kayip_Ciro'] / 1e6):
    ax2_twin.annotate(f"${y:.2f}M", (i, y), textcoords="offset points", xytext=(0, 8), 
                      ha='center', fontsize=10, fontweight='bold', color='#1f77b4')

plt.tight_layout()
plt.show()