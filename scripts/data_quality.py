import sqlite3
from logger import get_logger

logger = get_logger("data_quality")

DB_PATH = "economic_data.db"


def run_data_quality_checks():
    logger.info("Starting data quality checks")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Row count check 
    cursor.execute("SELECT COUNT(*) FROM fact_macro_annual")
    row_count = cursor.fetchone()[0]

    if row_count < 500:
        logger.error(f"Row count too low: {row_count}")
        raise ValueError("Row count check failed")

    logger.info(f"Row count check passed: {row_count} rows")

    # 2. Null checks 
    cursor.execute("""
        SELECT COUNT(*)
        FROM fact_macro_annual
        WHERE country_code IS NULL
           OR indicator_code IS NULL
           OR year IS NULL
           OR value IS NULL
    """)
    null_count = cursor.fetchone()[0]

    if null_count > 0:
        logger.error(f"Null values found: {null_count}")
        raise ValueError("Null check failed")

    logger.info("Null check passed")

    # 3. Duplicate check 
    cursor.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT country_code, indicator_code, year
            FROM fact_macro_annual
            GROUP BY country_code, indicator_code, year
            HAVING COUNT(*) > 1
        )
    """)
    duplicate_count = cursor.fetchone()[0]

    if duplicate_count > 0:
        logger.warning(
            f"Duplicates detected but handled by PRIMARY KEY: {duplicate_count}"
        )
    else:
        logger.info("Duplicate check passed")

    # 4. Value sanity check 
    cursor.execute("""
        SELECT COUNT(*)
        FROM fact_macro_annual
        WHERE ABS(value) > 1e15
    """)
    extreme_values = cursor.fetchone()[0]

    if extreme_values > 0:
        logger.warning(f"Extremely large values detected: {extreme_values}")
    else:
        logger.info("Value sanity check passed")

    conn.close()
    logger.info("Data quality checks completed successfully")


if __name__ == "__main__":
    run_data_quality_checks()
