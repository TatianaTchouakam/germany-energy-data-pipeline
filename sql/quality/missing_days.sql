-- Data quality check: missing or incomplete days over the backfill period,
-- grouped into continuous periods, with the backfill command to relaunch each one.
-- An empty result means the data is complete.
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
),
problem_days AS (
  SELECT
    e.day,
    IFNULL(l.rows_loaded, 0) AS rows_loaded
  FROM expected_days AS e
  LEFT JOIN loaded_days AS l USING (day)
  WHERE IFNULL(l.rows_loaded, 0) NOT IN (92, 96, 100)
),
grouped_days AS (
  SELECT
    day,
    rows_loaded,
    DATE_SUB(day, INTERVAL ROW_NUMBER() OVER (ORDER BY day) DAY) AS group_key
  FROM problem_days
)
SELECT
  MIN(day) AS start_day,
  MAX(day) AS end_day,
  COUNT(*) AS number_of_days,
  STRING_AGG(DISTINCT CAST(rows_loaded AS STRING)) AS rows_found,
  CONCAT(
    "python ingestion/backfill.py --start ", CAST(MIN(day) AS STRING),
    " --end ", CAST(MAX(day) AS STRING)
  ) AS backfill_command
FROM grouped_days
GROUP BY group_key
ORDER BY start_day;
