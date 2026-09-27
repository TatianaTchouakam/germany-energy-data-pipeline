-- Quarter-hours with a day-ahead price below 5 €/MWh on 21 September 2026 (Berlin time)
SELECT
  DATETIME(timestamp_utc, "Europe/Berlin") AS time_berlin,
  solar_mw,
  price_eur_mwh
FROM `tatiana-energy-pipeline.energy.generation_prices`
WHERE DATE(timestamp_utc, "Europe/Berlin") = "2026-09-21"
  AND price_eur_mwh < 5
ORDER BY time_berlin;
