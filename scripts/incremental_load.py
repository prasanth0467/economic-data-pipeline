import sqlite3
from logger import get_logger

logger = get_logger("incremental_load")

DB_PATH = "economic_data.db"


def run_incremental_load():
    logger.info("Starting incremental load")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get last loaded timestamp
    cur.execute("""
        SELECT COALESCE(MAX(ingested_at), '1900-01-01')
        FROM fact_macro_annual
    """)
    last_loaded_ts = cur.fetchone()[0]

    logger.info(f"Last loaded timestamp: {last_loaded_ts}")

    # Insert new records only
    cur.execute("""
        INSERT INTO fact_macro_annual (
            country_code,
            indicator_code,
            year,
            value,
            ingested_at
        )
        SELECT
            country_code,
            indicator_code,
            year,
            value,
            ingested_at
        FROM raw_macro_data
        WHERE ingested_at > ?
          AND value IS NOT NULL
          AND country_code IS NOT NULL
          AND indicator_code IS NOT NULL
          AND year IS NOT NULL
    """, (last_loaded_ts,))

    rows_inserted = cur.rowcount

    conn.commit()
    conn.close()

    logger.info(f"Incremental load completed. {rows_inserted} new records inserted.")


if __name__ == "__main__":
    try:
        run_incremental_load()
    except Exception:
        logger.error("Incremental load failed", exc_info=True)
        raise
