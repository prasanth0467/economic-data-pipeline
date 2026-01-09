create database economic_data;
use economic_data;
CREATE TABLE IF NOT EXISTS raw_macro_data (
    country TEXT,
    country_code TEXT,
    indicator_code TEXT,
    indicator_name TEXT,
    date TEXT,
    value REAL,
    source TEXT,
    ingested_at TEXT
);
CREATE TABLE IF NOT EXISTS pipeline_log (
    source TEXT,
    last_loaded_date TEXT,
    load_timestamp TEXT
); 
CREATE TABLE IF NOT EXISTS macro_indicators_fact AS
SELECT
    country,
    indicator_name,
    date,
    value,
    source
FROM raw_macro_data;
DROP TABLE IF EXISTS macro_indicators_fact;

CREATE TABLE macro_indicators_fact AS
SELECT DISTINCT
    country,
    indicator_code,
    indicator_name,
    date,
    value,
    source
FROM raw_macro_data
WHERE source = 'World Bank';


