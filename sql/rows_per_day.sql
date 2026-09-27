-- Data quality check: each day should have 96 quarter-hours
SELECT
  DATE(timestamp_utc, "Europe/Berlin") AS day_berlin,
  COUNT(*) AS rows_per_day
FROM `tatiana-energy-pipeline.energy.generation_prices`
GROUP BY day_berlin
ORDER BY day_berlin;
