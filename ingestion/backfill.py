"""Load a range of past days into BigQuery, one day at a time (backfill)."""
import argparse
import time
from datetime import date, timedelta
from pathlib import Path

from fetch_data import build_table
from load_to_gcp import load_to_bigquery, upload_to_gcs

PAUSE_BETWEEN_DAYS = 5
PAUSE_BEFORE_RETRY = 60


def daterange(start, end):
    """Yield every day from start to end, both included."""
    day = start
    while day <= end:
        yield day
        day += timedelta(days=1)


def load_day(day_str, output_folder):
    """Fetch one day, save it as CSV, upload it to GCS and load it into BigQuery."""
    df = build_table(day_str)
    file_path = output_folder / f"energy_{day_str}.csv"
    df.to_csv(file_path, index=False)
    gcs_uri = upload_to_gcs(file_path)
    return load_to_bigquery(
        gcs_uri,
        int(df["unix_seconds"].min()),
        int(df["unix_seconds"].max()),
    )


def load_days(days, output_folder):
    """Load a list of days and return the ones that failed."""
    failed_days = []
    for day_str in days:
        try:
            rows = load_day(day_str, output_folder)
            print(f"{day_str}: {rows} rows loaded")
        except Exception as error:
            print(f"{day_str}: FAILED ({error})")
            failed_days.append(day_str)
        time.sleep(PAUSE_BETWEEN_DAYS)
    return failed_days


def main():
    parser = argparse.ArgumentParser(description="Backfill German energy data day by day.")
    parser.add_argument("--start", required=True, help="First day, format YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Last day, format YYYY-MM-DD")
    args = parser.parse_args()

    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    days = [day.isoformat() for day in daterange(start, end)]

    output_folder = Path("data/processed")
    output_folder.mkdir(parents=True, exist_ok=True)

    failed_days = load_days(days, output_folder)

    if failed_days:
        print(f"\n{len(failed_days)} day(s) failed. Waiting {PAUSE_BEFORE_RETRY}s before one retry...")
        time.sleep(PAUSE_BEFORE_RETRY)
        failed_days = load_days(failed_days, output_folder)

    print(f"\nDone. {len(failed_days)} failed day(s): {failed_days}")


if __name__ == "__main__":
    main()
