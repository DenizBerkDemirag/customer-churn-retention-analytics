import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('cleaned_telecom_customer_churn.csv')

# Kolon isimlerindeki boşlukları PostgreSQL standartlarına uygun olarak alt çizgiye çevirmek.
df.columns = [col.strip().replace(' ', '_').lower() for col in df.columns]

# PostgreSQL Bağlantı Dizesi
db_user = 'Churn_Analysis'
db_password = 'Churn_Analysis'
db_host = 'localhost'
db_port = '5432'
db_name = "telecom_dw"

# Format: postgresql+psycopg2://KULLANICI_ADI:SIFRE@localhost:5432/telecom_dw
connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(connection_string)

print("Veri PostgreSQL veritabanına aktarılıyor...")
df.to_sql('stg_telecom_churn', engine, if_exists='replace', index=False)
print("Veri aktarıldı.")