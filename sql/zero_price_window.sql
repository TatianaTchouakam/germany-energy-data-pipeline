-- First and last quarter-hour at 0 €/MWh or below, and total duration, on 21 September 2026
SELECT
  MIN(DATETIME(timestamp_utc, "Europe/Berlin")) AS first_zero_price,
  MAX(DATETIME(timestamp_utc, "Europe/Berlin")) AS last_zero_price,
  COUNT(*) * 15 AS minutes_at_zero_or_below
FROM `tatiana-energy-pipeline.energy.generation_prices`
WHERE DATE(timestamp_utc, "Europe/Berlin") = "2026-09-21"
  AND price_eur_mwh <= 0;
