"""Fetch German wind, solar and day-ahead price data from Energy-Charts for one day.

Data source: Energy-Charts.info (Fraunhofer ISE), license CC BY 4.0.
"""
import argparse
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://api.energy-charts.info"

GENERATION_COLUMNS = {
    "Wind offshore": "wind_offshore_mw",
    "Wind onshore": "wind_onshore_mw",
    "Solar": "solar_mw",
}

def fetch_json(endpoint, params):
    """Call one Energy-Charts endpoint and return its JSON answer."""
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


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
    args = parser.parse_args()

    df = build_table(args.date)

    output_folder = Path("data/processed")
    output_folder.mkdir(parents=True, exist_ok=True)
    file_path = output_folder / f"energy_{args.date}.csv"
    df.to_csv(file_path, index=False)

    print(f"Saved {len(df)} rows to {file_path}")
    print(df.head())


if __name__ == "__main__":
    main()
    