import os
import sys
from pathlib import Path
from sqlalchemy import text

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_db import engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sql_files = [
    PROJECT_ROOT / "sql" / "01_star_schema_ddl.sql",
    PROJECT_ROOT / "sql" / "02_powerbi_view.sql"
]

def run_sql_pipeline():
    print("Executing SQL Pipeline...\n")
    
    with engine.begin() as conn:
        for file_path in sql_files:
            if not file_path.exists():
                print(f"File not found: {file_path}")
                continue
            
            print(f"-> Reading and executing: {file_path.name}...")
            with open(file_path, "r", encoding="utf-8") as f:
                sql_script = f.read()
            
            # Execute script on PostgreSQL
            conn.execute(text(sql_script))
            print(f"{file_path.name} executed successfully.\n")
            
    print("Star Schema tables and Power BI analytical view are ready!")

if __name__ == "__main__":
    run_sql_pipeline()