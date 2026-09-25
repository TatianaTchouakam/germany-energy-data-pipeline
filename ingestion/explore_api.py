"""Explore the Energy-Charts API endpoints and save sample responses.

Data source: Energy-Charts.info (Fraunhofer ISE), license CC BY 4.0.
"""

import json
from pathlib import Path

import requests

BASE_URL = "https://api.energy-charts.info"
START = "2026-09-20"
END = "2026-09-21"

endpoints = {
    "public_power": {"country": "de", "start": START, "end": END},
    "price": {"bzn": "DE-LU", "start": START, "end": END},
}

output_folder = Path("data/samples")
output_folder.mkdir(parents=True, exist_ok=True)

for name, params in endpoints.items():
    response = requests.get(f"{BASE_URL}/{name}", params=params, timeout=30)
    print(f"\n=== {name} | HTTP status {response.status_code} ===")
    response.raise_for_status()
    data = response.json()

    file_path = output_folder / f"{name}.json"
    file_path.write_text(json.dumps(data, indent=2))

    print("Keys:", list(data.keys()))
    timestamps = data.get("unix_seconds", [])
    print("Number of timestamps:", len(timestamps))
    if len(timestamps) > 1:
        print("Step between timestamps (seconds):", timestamps[1] - timestamps[0])