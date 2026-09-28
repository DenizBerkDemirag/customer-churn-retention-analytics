import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Temizlenmiş veriyi oku
df = pd.read_csv("data/cleaned/cleaned_telecom_customer_churn.csv")

# 2. Tenure_Group sıralamasını sabitle
order = ['0-6 Ay (Kritik)', '7-12 Ay', '1-2 Yıl', '2-4 Yıl', '4+ Yıl (Sadık)']
df["Tenure_Group"] = pd.Categorical(df['Tenure_Group'], categories=order, ordered=True)

# 3. İlgili metrikleri hesapla
summary = df.groupby("Tenure_Group", observed=False).agg(
    Toplam_Musteri=("Customer ID", "count"),
    Churn_Musteri=("Is_Churned", "sum"),
    Churn_Orani=("Is_Churned", lambda x: round(x.mean()*100,2))
)

# 4. Grafik alanını oluştur (Yan yana 2 grafik)
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
sns.set_theme(style="whitegrid")


# --- GRAFİK 1: Gruplara Göre Churn Oranı (%) ---
sns.barplot(data=summary, x="Tenure_Group", y="Churn_Orani", palette="Reds_r", ax=axes[0])
axes[0].set_title("Gruplara göre Churn Oranı(%)", fontsize=13, fontweight="bold", pad=12)
axes[0].set_ylabel("Churn Oranı(%)", fontsize=11)
axes[0].set_xlabel("")
axes[0].set_ylim(0, 100)

for p in axes[0].patches:
    axes[0].annotate(
        f"%{p.get_height():.1f}",
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='center',
        xytext=(0, 7),
        textcoords='offset points',
        fontweight='bold',
        fontsize=11
    )

# --- GRAFİK 2: Toplam Müşteri ve Kayıp Sayısı ---
summary = summary.reset_index()

summary_melted = pd.melt(
    summary, 
    id_vars=['Tenure_Group'], 
    value_vars=['Toplam_Musteri', 'Churn_Musteri'],
    var_name='Metrik', 
    value_name='Sayı'
)
summary_melted['Metrik'] = summary_melted['Metrik'].replace({
    'Toplam_Musteri': 'Toplam Müşteri', 
    'Churn_Musteri': 'Ayrılan (Churn)'
})

sns.barplot(
    data=summary_melted, 
    x='Tenure_Group', 
    y='Sayı', 
    hue='Metrik', 
    palette=['#337ab7', '#d9534f'], 
    ax=axes[1]
)
axes[1].set_title('Toplam Müşteri ve Kayıp Sayısı', fontsize=13, fontweight='bold', pad=12)
axes[1].set_ylabel('Kişi Sayısı', fontsize=11)
axes[1].set_xlabel('')
axes[1].legend(title='', fontsize=10)

plt.tight_layout()
plt.show()