"""Turn the price sample into a readable table with Berlin time."""
import json
from pathlib import Path
import pandas as pd

data = json.loads(Path("data/samples/price.json").read_text())

df= pd.DataFrame({
    "unix_seconds": data["unix_seconds"],
    "price_eur_mwh": data["price"],
})

df["timestamp_utc"] = pd.to_datetime(df["unix_seconds"], unit="s", utc=True)
df["timestamp_berlin"] = df["timestamp_utc"].dt.tz_convert("Europe/Berlin")

print(df.head(10))
print("\nlowest price:")
print(df.loc[df["price_eur_mwh"].idxmin()])
print("\nHighest price:")
print(df.loc[df["price_eur_mwh"].idxmax()])
