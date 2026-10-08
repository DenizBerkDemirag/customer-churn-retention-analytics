import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('telecom_customer_churn_clean.csv')

internet_df = df[df['Internet Service'] == 'Yes'].copy()
addon_summary = internet_df.groupby('Total_Addon_Services').agg(
    Toplam_Musteri=('Customer ID', 'count'),
    Churn_Orani=('Is_Churned', lambda x: round(x.mean() * 100, 1))
).reset_index()

def categorize_service_depth(row):
    if row['Internet Service'] == 'No':
        return '1. İnternet Hizmeti Yok\n(Sadece Sabit Hat)'
    elif row['Total_Addon_Services'] == 0:
        return '2. Yalın İnternet\n(0 Ek Hizmet)'
    elif row['Total_Addon_Services'] <= 3:
        return '3. Düşük Entegrasyon\n(1-3 Ek Hizmet)'
    else:
        return '4. Tam Ekosistem\n(4-7 Ek Hizmet)'

df['Service_Depth'] = df.apply(categorize_service_depth, axis=1)

depth_order = [
    '1. İnternet Hizmeti Yok\n(Sadece Sabit Hat)',
    '2. Yalın İnternet\n(0 Ek Hizmet)',
    '3. Düşük Entegrasyon\n(1-3 Ek Hizmet)',
    '4. Tam Ekosistem\n(4-7 Ek Hizmet)'
]
depth_summary = df.groupby('Service_Depth').agg(
    Toplam_Musteri=('Customer ID', 'count'),
    Churn_Orani=('Is_Churned', lambda x: round(x.mean() * 100, 1))
).reindex(depth_order).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.set_theme(style="whitegrid")

colors_p1 = ['#d9534f' if x == 0 else ('#f0ad4e' if x <= 3 else '#5cb85c') for x in addon_summary['Total_Addon_Services']]
bars1 = axes[0].bar(addon_summary['Total_Addon_Services'], addon_summary['Churn_Orani'], 
                     color=colors_p1, width=0.65, edgecolor='black', alpha=0.85)

axes[0].set_title('İnternet Abonelerinde Ek Hizmet Sayısına Göre Churn Oranı (%)\n(Sadece İnternet Kullanan 5.517 Müşteri)', fontsize=13, fontweight='bold', pad=14)
axes[0].set_xlabel('Alınan Ek Hizmet Sayısı (Güvenlik, Yedekleme, TV vb.)', fontsize=11)
axes[0].set_ylabel('Churn Oranı (%)', fontsize=11)
axes[0].set_xticks(range(0, 8))
axes[0].set_ylim(0, 60)

for bar in bars1:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f'%{yval:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

axes[0].annotate('Yalın İnternet Alanların\nYarısı Ayrılıyor!', 
                 xy=(0, 50.4), xytext=(0.8, 54),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#c9302c')

colors_p2 = ['#777777', '#d9534f', '#f0ad4e', '#5cb85c']
bars2 = axes[1].bar(depth_summary['Service_Depth'], depth_summary['Churn_Orani'], 
                     color=colors_p2, width=0.55, edgecolor='black', alpha=0.85)

axes[1].set_title('Hizmet Derinliği Segmentleri ve Churn Karşılaştırması\n(Tüm Portföy - 7.043 Müşteri)', fontsize=13, fontweight='bold', pad=14)
axes[1].set_xlabel('Müşteri Hizmet Segmenti', fontsize=11)
axes[1].set_ylabel('Churn Oranı (%)', fontsize=11)
axes[1].set_ylim(0, 60)

for bar in bars2:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f'%{yval:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

for bar, total in zip(bars2, depth_summary['Toplam_Musteri']):
    axes[1].text(bar.get_x() + bar.get_width()/2.0, 4, f'N={total:,}', ha='center', va='bottom', fontsize=9, color='white', fontweight='bold')

plt.tight_layout()
plt.show()