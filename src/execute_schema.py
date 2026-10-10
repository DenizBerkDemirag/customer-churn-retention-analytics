import os
import sys
from sqlalchemy import text

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_db import engine

sql_files = [
    "sql/01_star_schema_ddl.sql",
    "sql/02_powerbi_view.sql"
]

def run_sql_pipeline():
    print("🚀 SQL Pipeline başlatılıyor...\n")
    
    with engine.begin() as conn:
        for file_path in sql_files:
            if not os.path.exists(file_path):
                print(f"❌ Dosya bulunamadı: {file_path}")
                continue
            
            print(f"-> {file_path} dosyası okunuyor ve çalıştırılıyor...")
            with open(file_path, "r", encoding="utf-8") as f:
                sql_script = f.read()
            
            # Scripti PostgreSQL üzerinde yürüt
            conn.execute(text(sql_script))
            print(f"✅ {file_path} başarıyla tamamlandı.\n")
            
    print("🎉 Yıldız Şema tabloları ve Power BI View'ı başarıyla hazırlandı!")

if __name__ == "__main__":
    run_sql_pipeline()