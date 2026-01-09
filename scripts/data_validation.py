import sqlite3
import pandas as pd

conn = sqlite3.connect("economic_data.db")
df = pd.read_sql("SELECT * FROM raw_macro_data", conn)

# NULL checks 
wb_df = df[df["source"] == "World Bank"]
fred_df = df[df["source"] == "FRED"]

assert wb_df[["country", "indicator_code", "date"]].isnull().sum().sum() == 0, \
    "Nulls found in World Bank identifiers"

assert fred_df[["series_id", "date"]].isnull().sum().sum() == 0, \
    "Nulls found in FRED identifiers"

print("Raw layer validation passed (duplicates allowed).")

conn.close()
