-- Gold layer: one row per day (Berlin time) with price and generation indicators
SELECT
  day_berlin,
  COUNT(*) AS quarter_hours,
  ROUND(AVG(price_eur_mwh), 2) AS avg_price_eur_mwh,
  MIN(price_eur_mwh) AS min_price_eur_mwh,
  MAX(price_eur_mwh) AS max_price_eur_mwh,
  ROUND(MAX(price_eur_mwh) - MIN(price_eur_mwh), 2) AS price_spread_eur_mwh,
  COUNTIF(price_eur_mwh <= 0) AS zero_or_negative_price_quarter_hours,
  ROUND(SUM(solar_mw) * 0.25 / 1000, 1) AS solar_gwh,
  ROUND(SUM(wind_total_mw) * 0.25 / 1000, 1) AS wind_gwh,
  ROUND(MAX(solar_mw) / 1000, 1) AS solar_peak_gw
FROM `tatiana-energy-pipeline.energy.stg_generation_prices`
GROUP BY day_berlin
