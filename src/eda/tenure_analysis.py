from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / "cleaned_telecom_customer_churn.csv"

# 1. Load cleaned dataset
df = pd.read_csv(DATA_PATH)

# 2. Fix Tenure_Group categorical order
order = ['0-6 Months (Critical)', '7-12 Months', '1-2 Years', '2-4 Years', '4+ Years (Loyal)']
df["Tenure_Group"] = pd.Categorical(df['Tenure_Group'], categories=order, ordered=True)

# 3. Calculate metrics by tenure group
summary = df.groupby("Tenure_Group", observed=False).agg(
    Total_Customers=("Customer ID", "count"),
    Churned_Customers=("Is_Churned", "sum"),
    Churn_Rate=("Is_Churned", lambda x: round(x.mean() * 100, 2))
)

# 4. Create 2-panel figure
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
sns.set_theme(style="whitegrid")

# --- CHART 1: Churn Rate by Tenure Group (%) ---
sns.barplot(data=summary, x="Tenure_Group", y="Churn_Rate", hue="Tenure_Group", palette="Reds_r", legend=False, ax=axes[0])
axes[0].set_title("Churn Rate by Tenure Group (%)", fontsize=13, fontweight="bold", pad=12)
axes[0].set_ylabel("Churn Rate (%)", fontsize=11)
axes[0].set_xlabel("")
axes[0].set_ylim(0, 100)

for p in axes[0].patches:
    axes[0].annotate(
        f"{p.get_height():.1f}%",
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='center',
        xytext=(0, 7),
        textcoords='offset points',
        fontweight='bold',
        fontsize=11
    )

# --- CHART 2: Total Customers vs Churned Customers ---
summary = summary.reset_index()

summary_melted = pd.melt(
    summary, 
    id_vars=['Tenure_Group'], 
    value_vars=['Total_Customers', 'Churned_Customers'],
    var_name='Metric', 
    value_name='Count'
)
summary_melted['Metric'] = summary_melted['Metric'].replace({
    'Total_Customers': 'Total Customers', 
    'Churned_Customers': 'Churned Customers'
})

sns.barplot(
    data=summary_melted, 
    x='Tenure_Group', 
    y='Count', 
    hue='Metric', 
    palette=['#337ab7', '#d9534f'], 
    ax=axes[1]
)
axes[1].set_title('Total Customers vs. Churned Customers', fontsize=13, fontweight='bold', pad=12)
axes[1].set_ylabel('Customer Count', fontsize=11)
axes[1].set_xlabel('')
axes[1].legend(title='', fontsize=10)

plt.tight_layout()
plt.show()