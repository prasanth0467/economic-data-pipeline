import requests
import sqlite3
from datetime import datetime, UTC
from logger import get_logger
logger = get_logger("ingest_worldbank")

DB_PATH = "economic_data.db"

INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP (current USD)",
    "FP.CPI.TOTL": "Inflation (CPI)",
    "SL.UEM.TOTL.ZS": "Unemployment Rate"
}

COUNTRIES = ["IND", "USA", "CHN", "DEU", "JPN"]
PER_PAGE = 200



def run_worldbank_ingestion():
    logger.info("Starting World Bank ingestion")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS raw_macro_data;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_macro_data (
            country TEXT,
            country_code TEXT,
            indicator_code TEXT,
            indicator_name TEXT,
            year INTEGER,
            value REAL,
            source TEXT,
            ingested_at TEXT
        )
    """)

    total_records = 0

    for indicator_code, indicator_name in INDICATORS.items():
        logger.info(f"Fetching indicator: {indicator_code} ({indicator_name})")

        page = 1
        while True:
            url = (
                f"https://api.worldbank.org/v2/country/"
                f"{';'.join(COUNTRIES)}/indicator/{indicator_code}"
                f"?format=json&per_page={PER_PAGE}&page={page}"
            )

            response = requests.get(url, timeout=30).json()

            if len(response) < 2 or not response[1]:
                break

            for row in response[1]:
                if row["value"] is None:
                    continue

                cur.execute("""
                    INSERT INTO raw_macro_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row["country"]["value"],
                    row["country"]["id"],
                    indicator_code,
                    indicator_name,
                    int(row["date"]),
                    float(row["value"]),
                    "World Bank",
                    datetime.now(UTC).isoformat()
                ))

                total_records += 1

            page += 1

        logger.info(f"Completed indicator: {indicator_code}")

    conn.commit()
    conn.close()

    logger.info(f"World Bank ingestion completed successfully. Total records: {total_records}")


if __name__ == "__main__":
    try:
        run_worldbank_ingestion()
    except Exception:
        logger.error("World Bank ingestion failed", exc_info=True)
        raise
