import os
import pandas as pd
from sqlalchemy import create_engine

csv_path = 'cleaned_telecom_customer_churn.csv'

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Dosya bulunamadı: {csv_path}")

print("CSV dosyası okunuyor...")
df = pd.read_csv(csv_path)

# Kolon isimlerindeki boşlukları PostgreSQL standartlarına uygun olarak alt çizgiye çevirmek.
df.columns = [
    col.strip()
       .lower()
       .replace(' ', '_')
       .replace('/', '_')
       .replace('-', '_')
    for col in df.columns
]

# PostgreSQL Bağlantı Dizesi
db_user = 'Churn_Analysis'
db_password = 'Churn_Analysis'
db_host = 'localhost'
db_port = '5432'
db_name = "telecom_dw"

# Format: postgresql+psycopg2://KULLANICI_ADI:SIFRE@localhost:5432/telecom_dw
connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(connection_string)

# Veriyi PostgreSQL'e Aktarmak.
try:
    print(f"Veriler '{db_name}' veritabanındaki 'stg_telecom_churn' tablosuna aktarılıyor...")
    
    # if_exists='replace' -> Tablo varsa önce siler, sonra sıfırdan oluşturup doldurur
    # chunksize=1000 -> Veriyi 1000'er satırlık paketler halinde hızlıca yükler
    df.to_sql('stg_telecom_churn', engine, if_exists='replace', index=False, chunksize=1000)
    
    print("✅ Aktarım başarıyla tamamlandı!")
    print(f"Toplam {len(df):,} satır başarıyla yüklendi.")

except Exception as e:
    print(f"❌ Bir hata oluştu: {e}")