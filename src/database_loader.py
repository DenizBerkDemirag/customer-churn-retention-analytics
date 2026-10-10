import os
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_db import engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "cleaned" / "cleaned_telecom_customer_churn.csv"

def load_staging_data(csv_file_path: Path | str = DEFAULT_CSV_PATH):
    csv_path = Path(csv_file_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    print(f"1. Reading cleaned CSV dataset: {csv_path}")
    df = pd.read_csv(csv_path)

    df.columns = [
        col.strip()
           .lower()
           .replace(' ', '_')
           .replace('/', '_')
           .replace('-', '_')
        for col in df.columns
    ]

    print(f"2. Loading data into PostgreSQL 'stg_telecom_churn' table (Rows: {len(df):,})...")
    
    df.to_sql(
        name='stg_telecom_churn',
        con=engine,
        if_exists='replace',
        index=False,
        chunksize=1000
    )
    print("Staging table successfully populated and loaded!\n")

if __name__ == "__main__":
    load_staging_data()