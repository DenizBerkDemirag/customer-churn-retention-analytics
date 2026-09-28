import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/cleaned/cleaned_telecom_customer_churn.csv")

ref_analysis = df.groupby("Number of Referrals").agg(
    Toplam_Musteri=("Customer ID", "count"),
    Churn_Sayisi=("Is_Churned", "sum"),
    Churn_Orani=("Is_Churned", lambda x: round(x.mean()*100,2))
).reset_index()

ref_group_analysis = df.groupby("Referral_Group", observed=False).agg(
    Toplam_Musteri=("Customer ID", "count"),
    Churn_Orani=("Is_Churned", lambda x: round(x.mean()*100,2))
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
sns.set_theme(style="whitegrid")

axes[0].plot(ref_analysis["Number of Referrals"], ref_analysis["Churn_Orani"], marker='o', color='#c9302c', linewidth=2.5, markersize=7)
axes[0].set_title('Tavsiye Sayısına Göre Churn Oranı Eğrisi (%)', fontsize=13, fontweight='bold', pad=12)
axes[0].set_xlabel('Verilen Referans Sayısı (Number of Referrals)')
axes[0].set_ylabel('Churn Oranı (%)')
axes[0].set_xticks(range(0, 12))
axes[0].set_ylim(-2, 50)
axes[0].grid(True, linestyle=':', alpha=0.6)

for x, y in zip(ref_analysis['Number of Referrals'], ref_analysis['Churn_Orani']):
    axes[0].annotate(f"%{y:.1f}",
                    (x, y),
                    textcoords="offset points", xytext=(0, 8), 
                    ha='center', fontsize=9, fontweight='bold')


ax2_twin = axes[1].twinx()

sns.barplot(data=ref_group_analysis, x='Referral_Group', y='Toplam_Musteri', palette='Blues_d', ax=axes[1], alpha=0.85)
axes[1].set_title('Referans Segmentleri: Müşteri Hacmi vs. Churn Oranı', fontsize=13, fontweight='bold', pad=12)
axes[1].set_xlabel('Referans Segmenti')
axes[1].set_ylabel('Toplam Müşteri Sayısı', color='#1f77b4')
axes[1].grid(False)


ax2_twin.plot(range(len(ref_group_analysis)), ref_group_analysis['Churn_Orani'], color='#d9534f', marker='s', linewidth=2.5, markersize=8)
ax2_twin.set_ylabel('Churn Oranı (%)', color='#d9534f')
ax2_twin.set_ylim(0, 50)
ax2_twin.grid(True, linestyle=':', alpha=0.5)

for i, y in enumerate(ref_group_analysis['Churn_Orani']):
    ax2_twin.annotate(f"%{y:.1f}", (i, y), textcoords="offset points", xytext=(0, 9), 
                      ha='center', fontsize=10, fontweight='bold', color='#d9534f')

plt.tight_layout()
plt.show()