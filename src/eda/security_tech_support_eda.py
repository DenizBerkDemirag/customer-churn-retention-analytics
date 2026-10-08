import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('telecom_customer_churn_clean.csv')

def combo_group(row):
    sec = row['Online Security']
    tech = row['Premium Tech Support']
    if sec == 'No Internet Service' or tech == 'No Internet Service':
        return 'İnternet Yok\n(Referans)'
    elif sec == 'Yes' and tech == 'Yes':
        return 'İkisi de Var\n(Tam Koruma)'
    elif sec == 'Yes' and tech == 'No':
        return 'Sadece\nSecurity'
    elif sec == 'No' and tech == 'Yes':
        return 'Sadece\nTech Support'
    else:
        return 'İkisi de Yok\n(Hiçbiri)'

df['Security_Support_Combo'] = df.apply(combo_group, axis=1)

combo_order = [
    'İkisi de Yok\n(Hiçbiri)',
    'Sadece\nSecurity',
    'Sadece\nTech Support',
    'İkisi de Var\n(Tam Koruma)',
    'İnternet Yok\n(Referans)'
]

combo_stats = df.groupby('Security_Support_Combo').agg(
    Toplam_Musteri=('Customer ID', 'count'),
    Churn_Orani=('Is_Churned', lambda x: round(x.mean() * 100, 1))
).reindex(combo_order).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.set_theme(style="whitegrid")

internet_df = df[df['Internet Service'] == 'Yes'].copy()
sec_comp = internet_df.groupby('Online Security')['Is_Churned'].mean().reset_index()
sec_comp['Hizmet'] = 'Online Security'
tech_comp = internet_df.groupby('Premium Tech Support')['Is_Churned'].mean().reset_index()
tech_comp['Hizmet'] = 'Premium Tech Support'

single_df = pd.concat([
    sec_comp.rename(columns={'Online Security': 'Durum'}),
    tech_comp.rename(columns={'Premium Tech Support': 'Durum'})
])
single_df['Churn_Orani'] = single_df['Is_Churned'] * 100

sns.barplot(data=single_df, x='Hizmet', y='Churn_Orani', hue='Durum', 
            palette=['#d9534f', '#5cb85c'], ax=axes[0], edgecolor='black', alpha=0.85)
axes[0].set_title('İnternet Abonelerinde Hizmet Bazlı Churn Oranı (%)\n(Alanlar vs Almayanlar)', fontsize=13, fontweight='bold', pad=14)
axes[0].set_ylabel('Churn Oranı (%)')
axes[0].set_xlabel('')
axes[0].set_ylim(0, 50)
axes[0].legend(title='Hizmet Durumu', loc='upper right')

for p in axes[0].patches:
    h = p.get_height()
    if h > 0:
        axes[0].annotate(f"%{h:.1f}", (p.get_x() + p.get_width() / 2., h), 
                         ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', 
                         fontweight='bold', fontsize=11)

colors_p2 = ['#d9534f', '#f0ad4e', '#f0ad4e', '#5cb85c', '#777777']
bars2 = axes[1].bar(combo_stats['Security_Support_Combo'], combo_stats['Churn_Orani'], 
                    color=colors_p2, edgecolor='black', alpha=0.85, width=0.6)

axes[1].set_title('Güvenlik ve Destek Paketlerinin Sinerji Etkisi (%)\n(Kombinasyon Analizi)', fontsize=13, fontweight='bold', pad=14)
axes[1].set_ylabel('Churn Oranı (%)')
axes[1].set_xlabel('')
axes[1].set_ylim(0, 60)

for bar in bars2:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f'%{yval:.1f}', 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

axes[1].annotate('En Yüksek Kayıp:\n1.250 Müşteri ($2.05M)', 
                 xy=(0, 49.0), xytext=(0.4, 53),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#c9302c')

plt.tight_layout()
plt.show()