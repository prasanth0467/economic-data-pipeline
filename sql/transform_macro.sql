CREATE TABLE IF NOT EXISTS fact_macro_annual (
    country_code TEXT NOT NULL,
    indicator_code TEXT NOT NULL,
    year INTEGER NOT NULL,
    value REAL,
    ingested_at TIMESTAMP,
    PRIMARY KEY (country_code, indicator_code, year)
);

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
WHERE source = 'World Bank'
  AND value IS NOT NULL
  AND country_code IS NOT NULL
  AND indicator_code IS NOT NULL
  AND year IS NOT NULL;
