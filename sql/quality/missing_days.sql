-- Data quality check: days that are missing or incomplete over the backfill period
WITH expected_days AS (
  SELECT day
  FROM UNNEST(GENERATE_DATE_ARRAY("2025-10-01", "2026-09-27")) AS day
),
loaded_days AS (
  SELECT
    DATE(timestamp_utc, "Europe/Berlin") AS day,
    COUNT(*) AS rows_loaded
  FROM `tatiana-energy-pipeline.energy.generation_prices`
  GROUP BY day
)
SELECT
  e.day,
  IFNULL(l.rows_loaded, 0) AS rows_loaded
FROM expected_days AS e
LEFT JOIN loaded_days AS l USING (day)
WHERE IFNULL(l.rows_loaded, 0) NOT IN (92, 96, 100)
ORDER BY e.day;
