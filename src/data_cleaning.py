import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_CHURN_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "telco_customer_churn.csv"
RAW_ZIP_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "telecom_zipcode_popuplation.csv"
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "cleaned"

df_churn = pd.read_csv(RAW_CHURN_DATA_PATH)
df_zip = pd.read_csv(RAW_ZIP_DATA_PATH)

# 2. Negatif Monthly Charge Düzeltmesi
mask_neg = df_churn["MonthlyCharge"] < 0
df_churn.loc[mask_neg, "Monthly Charge"] = (
    df_churn.loc[mask_neg, "Total Charges"] / df_churn.loc[mask_neg, "Tenure in Months"]
).round(2)

# 3. Sayısal Boşluklar
df_churn["Avg Monthly Long Distance Charges"] = df_churn["Avg Monthly Long Distance Charges"].fillna(0)
df_churn["Avg Monthly GB Download"] = df_churn["Avg Monthly GB Download"].fillna(0)

# 4. Kategorik Boşluklar
df_churn["Multiple Lines"] = df_churn["Multiple Lines"].fillna("No Phone Service")
df_churn["Internet Type"] = df_churn["Internet Type"].fillna("No Internet Service")

sub_services = [
    'Online Security', 'Online Backup', 'Device Protection Plan',
    'Premium Tech Support', 'Streaming TV', 'Streaming Movies',
    'Streaming Music', 'Unlimited Data'
]

for col in sub_services:
    df_churn[col] = df_churn[col].fillna("No Internet Service")

df_churn["Offer"] = df_churn["Offer"].fillna("No Offer")
df_churn["Churn Category"] = df_churn["Churn Category"].fillna("No Applicable")
df_churn["Churn Reason"] = df_churn["Churn Reason"].fillna("No Applicable")

# 5. Yeni Özellikler (Feature Engineering)
df_churn["Is_Churned"] = (df_churn["Customer Status"] == "Churned").astype(int)

df_churn["Tenure_Group"] = pd.cut(
    df_churn["Tenure in Months"],
    bins=[0, 6, 12, 24, 48, 72],
    labels=['0-6 Ay (Kritik)', '7-12 Ay', '1-2 Yıl', '2-4 Yıl', '4+ Yıl (Sadık)']
)

df_churn['Age_Group'] = pd.cut(
    df_churn['Age'],
    bins=[18, 30, 50, 65, 100],
    labels=['Genç (19-30)', 'Orta Yaş (31-50)', 'Olgun (51-65)', 'Emekli (65+)']
)

df_churn['Referral_Group'] = pd.cut(
    df_churn['Number of Referrals'],
    bins=[-1, 0, 4, 11],
    labels=['0 Referans', '1-4 Referans', '5+ Referans (Elçi)']
)

addon_cols = ['Online Security', 'Online Backup', 'Device Protection Plan', 'Premium Tech Support', 'Streaming TV', 'Streaming Movies', 'Streaming Music']

df_churn['Total_Addon_Services'] = (df_churn[addon_cols] == 'Yes').sum(axis=1)

# 3. Gerçek Aylık Ortalama Gelir (ARPU)
df_churn["Monthly_ARPU"] = (df_churn["Total Revenue"] / df_churn["Tenure in Months"]).round(2)

df_clean = pd.merge(df_churn, df_zip, how="left")

df_clean.to_csv(CLEANED_DATA_PATH / "cleaned_telco_customer_churn.csv", index=False)