import requests
import pandas as pd
from datetime import datetime

API_KEY = "6314a59d9efefba2298e43f40d003f09"

SERIES = {
    "FEDFUNDS": "Federal Funds Rate",
    "CPIAUCSL": "CPI (All Urban Consumers)",
    "GS10": "10Y Treasury Yield",
    "GS2": "2Y Treasury Yield"
}

records = []

for series_id, series_name in SERIES.items():

    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}"
        f"&api_key={API_KEY}"
        "&file_type=json"
    )

    response = requests.get(url).json()

    # Defensive check (VERY important in industry)
    if "observations" not in response:
        print(f"Failed to fetch {series_id}: {response}")
        continue

    for obs in response["observations"]:
        if obs["value"] != ".":
            records.append({
                "series_id": series_id,
                "indicator_name": series_name,
                "date": obs["date"],
                "value": float(obs["value"]),
                "source": "FRED",
                "ingested_at": datetime.now()
            })

df = pd.DataFrame(records)
df.to_csv("fred_raw.csv", index=False)

print("FRED data ingestion completed successfully.")
