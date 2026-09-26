"""Turn the public_power sample into a readable table (wind, solar) with Berlin time."""

import json
from pathlib import Path
import pandas as pd

data=json.loads(Path("data/samples/public_power.json").read_text())

print("Available production types:")
for item in data["production_types"]:
    print("-", item["name"])
    
wanted =["Wind onshore", "Wind offshore", "Solar"]
df=pd.DataFrame({"unix_seconds": data["unix_seconds"]})
for item in data["production_types"]:
    if item["name"] in wanted:
        df[item["name"]]=item["data"]

df["timestamp_berlin"]=(
    pd.to_datetime(df["unix_seconds"], unit="s", utc=True)
    .dt.tz_convert("Europe/Berlin")
)

print(df.head(10))
print("\nSummary (values in MW):")
print(df.drop(columns=["unix_seconds"]).describe())