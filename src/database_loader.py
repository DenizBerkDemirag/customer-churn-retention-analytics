import os
import sys
import pandas as pd
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_db import engine

def load_staging_data(csv_file_path: str = "cleaned_telecom_customer_churn.csv"):
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"Dosya bulunamadı: {csv_file_path}")

    print(f"1. CSV dosyası okunuyor: {csv_file_path}")
    df = pd.read_csv(csv_file_path)

    df.columns = [
        col.strip()
           .lower()
           .replace(' ', '_')
           .replace('/', '_')
           .replace('-', '_')
        for col in df.columns
    ]

    print(f"2. Veriler PostgreSQL 'stg_telecom_churn' tablosuna aktarılıyor (Satır: {len(df):,})...")
    
    df.to_sql(
        name='stg_telecom_churn',
        con=engine,
        if_exists='replace',
        index=False,
        chunksize=1000
    )
    print("✅ Staging tablosu başarıyla oluşturuldu ve yüklendi!\n")

if __name__ == "__main__":
    load_staging_data()