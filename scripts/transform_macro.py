import sqlite3
from logger import get_logger

logger = get_logger("transform_macro")

DB_PATH = "economic_data.db"


def run_transform():
    logger.info("Starting macro transformation")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Drop fact table 
    cur.execute("DROP TABLE IF EXISTS fact_macro_annual;")

    # 2. Build fact table 
    cur.execute("""
        CREATE TABLE fact_macro_annual AS
        SELECT DISTINCT
            TRIM(country_code)   AS country_code,
            TRIM(indicator_code) AS indicator_code,
            CAST(year AS INTEGER) AS year,
            value,
            ingested_at
        FROM raw_macro_data
        WHERE value IS NOT NULL
          AND country_code IS NOT NULL
          AND indicator_code IS NOT NULL
          AND TRIM(country_code) <> ''
          AND TRIM(indicator_code) <> '';
    """)

    # 3. Build dim_country
    cur.execute("DROP TABLE IF EXISTS dim_country;")

    cur.execute("""
        CREATE TABLE dim_country AS
        SELECT DISTINCT
            country_code
        FROM fact_macro_annual;
    """)

    # 4. Build dim_indicator
    cur.execute("DROP TABLE IF EXISTS dim_indicator;")

    cur.execute("""
        CREATE TABLE dim_indicator AS
        SELECT DISTINCT
            indicator_code
        FROM fact_macro_annual;
    """)

    conn.commit()
    conn.close()

    logger.info("Macro transformation completed successfully")


if __name__ == "__main__":
    run_transform()
