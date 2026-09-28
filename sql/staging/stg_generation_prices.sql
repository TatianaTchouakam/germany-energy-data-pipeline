-- Silver layer: one row per quarter-hour, with Berlin time and total renewable generation
SELECT
  timestamp_utc,
  DATETIME(timestamp_utc, "Europe/Berlin") AS time_berlin,
  DATE(timestamp_utc, "Europe/Berlin") AS day_berlin,
  wind_onshore_mw,
  wind_offshore_mw,
  wind_onshore_mw + wind_offshore_mw AS wind_total_mw,
  solar_mw,
  wind_onshore_mw + wind_offshore_mw + solar_mw AS renewable_total_mw,
  price_eur_mwh
FROM `tatiana-energy-pipeline.energy.generation_prices`
