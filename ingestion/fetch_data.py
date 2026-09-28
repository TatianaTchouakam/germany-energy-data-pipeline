"""Fetch German wind, solar and day-ahead price data from Energy-Charts for one day.

Data source: Energy-Charts.info (Fraunhofer ISE), license CC BY 4.0.
"""
import argparse
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests
from load_to_gcp import load_to_bigquery, upload_to_gcs

BASE_URL = "https://api.energy-charts.info"

GENERATION_COLUMNS = {
    "Wind offshore": "wind_offshore_mw",
    "Wind onshore": "wind_onshore_mw",
    "Solar": "solar_mw",
}

MAX_ATTEMPTS = 5


def fetch_json(endpoint, params):
    """Call one Energy-Charts endpoint and return its JSON answer.

    Retries with increasing waits when the API says we are too fast (HTTP 429).
    """
    for attempt in range(1, MAX_ATTEMPTS + 1):
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        if response.status_code != 429:
            response.raise_for_status()
            return response.json()

        retry_after = response.headers.get("Retry-After", "")
        wait_seconds = int(retry_after) if retry_after.isdigit() else 10 * attempt
        print(f"Rate limited by the API, waiting {wait_seconds}s (attempt {attempt}/{MAX_ATTEMPTS})")
        time.sleep(wait_seconds)

    response.raise_for_status()


def fetch_prices(day):
    """Return a table of day-ahead prices (EUR/MWh) for one day."""
    data = fetch_json("price", {"bzn": "DE-LU", "start": day, "end": day})
    return pd.DataFrame({
        "unix_seconds": data["unix_seconds"],
        "price_eur_mwh": data["price"],
    })


def fetch_wind_solar(day):
    """Return a table of wind and solar generation (MW) for one day."""
    data = fetch_json("public_power", {"country": "de", "start": day, "end": day})
    df = pd.DataFrame({"unix_seconds": data["unix_seconds"]})
    for item in data["production_types"]:
        if item["name"] in GENERATION_COLUMNS:
            df[GENERATION_COLUMNS[item["name"]]] = item["data"]
    return df


def build_table(day):
    """Join generation and prices on the same timestamps."""
    generation = fetch_wind_solar(day)
    prices = fetch_prices(day)
    df = generation.merge(prices, on="unix_seconds", how="inner")
    df["timestamp_utc"] = pd.to_datetime(df["unix_seconds"], unit="s", utc=True)
    return df


def main():
    parser = argparse.ArgumentParser(description="Fetch one day of German energy data.")
    parser.add_argument(
        "--date",
        default=str(date.today() - timedelta(days=1)),
        help="Day to fetch, format YYYY-MM-DD (default: yesterday)",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Also upload the file to Cloud Storage and load it into BigQuery",
    )
    
    args = parser.parse_args()

    df = build_table(args.date)

    output_folder = Path("data/processed")
    output_folder.mkdir(parents=True, exist_ok=True)
    file_path = output_folder / f"energy_{args.date}.csv"
    df.to_csv(file_path, index=False)

    print(f"Saved {len(df)} rows to {file_path}")
    print(df.head())
    
    if args.upload:
        gcs_uri = upload_to_gcs(file_path)
        rows = load_to_bigquery(
            gcs_uri,
            int(df["unix_seconds"].min()),
            int(df["unix_seconds"].max()),
        )
        print(f"Uploaded to {gcs_uri} and loaded {rows} rows into BigQuery")

if __name__ == "__main__":
    main()
    