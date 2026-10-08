import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

df = pd.read_csv('telecom_customer_churn_clean.csv')

offer_summary = df.groupby('Offer').agg(
    Toplam_Musteri=('Customer ID', 'count'),
    Churn_Sayisi=('Is_Churned', 'sum'),
    Churn_Orani=('Is_Churned', lambda x: round(x.mean() * 100, 2)),
    Toplam_Kayip_Ciro=('Total Revenue', lambda x: round(x[df.loc[x.index, 'Is_Churned'] == 1].sum(), 2))
).reset_index().sort_values(by='Churn_Orani', ascending=False)

contingency_table = pd.crosstab(df['Offer'], df['Customer Status'])
chi2, p_val, dof, _ = chi2_contingency(contingency_table)
print(f"Chi2: {chi2:.4f}, p-value: {p_val:.4e}")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.set_theme(style="whitegrid")

palette_offer = ['#d9534f' if x > 30 else ('#f0ad4e' if x > 20 else '#5cb85c') for x in offer_summary['Churn_Orani']]
bars1 = axes[0].bar(offer_summary['Offer'], offer_summary['Churn_Orani'], 
                    color=palette_offer, edgecolor='black', alpha=0.85, width=0.55)

axes[0].set_title('Pazarlama Tekliflerine (Offer) Göre Churn Oranı (%)\n(En Riskli Kampanyadan En Başarılıya)', fontsize=13, fontweight='bold', pad=14)
axes[0].set_ylabel('Churn Oranı (%)', fontsize=11)
axes[0].set_xlabel('Pazarlama Teklifi (Offer)', fontsize=11)
axes[0].set_ylim(0, 65)

for bar in bars1:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f'%{yval:.1f}', 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

axes[0].annotate('En Başarısız Kampanya:\nHer 2 kişiden 1\'i ayrılıyor!', 
                 xy=(0, 52.9), xytext=(0.5, 58),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#c9302c')

axes[0].annotate('Altın Standart:\nSadece %6.7 Churn', 
                 xy=(5, 6.7), xytext=(4.2, 18),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#2b7b2b')

ax2_twin = axes[1].twinx()

sns.barplot(data=offer_summary, x='Offer', y='Toplam_Musteri', 
            palette='Blues_d', ax=axes[1], alpha=0.8, edgecolor='black')
axes[1].set_title('Kampanya Portföy Büyüklüğü vs. Toplam Kayıp Ciro ($)', fontsize=13, fontweight='bold', pad=14)
axes[1].set_xlabel('Pazarlama Teklifi (Offer)', fontsize=11)
axes[1].set_ylabel('Toplam Müşteri Sayısı', fontsize=11, color='#1f77b4')
axes[1].grid(False)

ax2_twin.plot(range(len(offer_summary)), offer_summary['Toplam_Kayip_Ciro'] / 1e6, 
              color='#d9534f', marker='s', linewidth=2.5, markersize=8)
ax2_twin.set_ylabel('Toplam Kayıp Ciro ($ Milyon)', fontsize=11, color='#d9534f')
ax2_twin.set_ylim(0, 2.5)
ax2_twin.grid(True, linestyle=':', alpha=0.5)

for i, y in enumerate(offer_summary['Toplam_Kayip_Ciro'] / 1e6):
    ax2_twin.annotate(f"${y:.2f}M", (i, y), textcoords="offset points", xytext=(0, 8), 
                      ha='center', fontsize=10, fontweight='bold', color='#d9534f')

plt.tight_layout()
plt.show()