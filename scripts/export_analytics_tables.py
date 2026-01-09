import sqlite3
import pandas as pd
import os
from logger import get_logger
logger = get_logger("export_analytics_tables")

DB_PATH = "economic_data.db"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

tables = {
    "fact_macro_annual": "fact_macro_annual.csv",
    "dim_country": "dim_country.csv",
    "dim_indicator": "dim_indicator.csv"
}

for table, filename in tables.items():
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    logger.info(f"DEBUG: DataFrame shape before export = {df.shape}")
    output_path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(output_path, index=False)
    print(f"Exported {table}: {len(df)} rows")

conn.close()

print("Analytics-ready exports completed successfully.")
