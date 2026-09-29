-- Key figures over the full period (1 Oct 2025 to the latest loaded day)
SELECT
  MIN(day_berlin) AS first_day,
  MAX(day_berlin) AS last_day,
  COUNT(*) AS days,
  ROUND(AVG(avg_price_eur_mwh), 2) AS avg_daily_price_eur_mwh,
  SUM(zero_or_negative_price_quarter_hours) AS zero_or_negative_quarter_hours,
  ROUND(SUM(zero_or_negative_price_quarter_hours) / 4, 1) AS zero_or_negative_hours,
  MIN(min_price_eur_mwh) AS lowest_price_eur_mwh,
  MAX(max_price_eur_mwh) AS highest_price_eur_mwh,
  ROUND(SUM(solar_gwh) / 1000, 1) AS solar_twh,
  ROUND(SUM(wind_gwh) / 1000, 1) AS wind_twh
FROM `tatiana-energy-pipeline.energy.mart_daily_summary`;
