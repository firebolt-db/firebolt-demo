--analytical query
USE ENGINE adtech_analytics;
USE DATABASE adtech;
SHOW TABLES;

--analytical query
WITH
  ltv AS (
    SELECT
      ltv.*,
      acc.name AS acc_name,
      acc.shipping_country,
      acc.region,
      app.name AS app_name,
      app.platform,
      app.app_slug,
      app.owner_account
    FROM
      ltv -- (57B rows)
      LEFT JOIN owned_apps AS app ON CITY_HASH (ltv.app_id) = CITY_HASH (app.app_slug)
      LEFT JOIN account AS acc ON CITY_HASH (acc.id) = CITY_HASH (app.owner_account)
  )
SELECT
  app_name,
  media_source,
  acc_name,
  shipping_country,
  region,
  platform,
  COALESCE(
    SUM(
      CASE
        WHEN (attribution_type = 'install') THEN clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (attribution_type = 'install') THEN impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (attribution_type = 'install') THEN installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (((ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01') AND (ltv_timestamp_dt) < (TIMESTAMP '2025-02-15')))
  AND ltv.media_source = '3bc36bb9f1bded2703684dae170581dc'
  --AND ltv.media_source = 'e391b3d1930968f4cce0d5dee539d256'
  --AND media_source = 'b935fcce8f277b6c60cd7598349c64e8'
GROUP BY ALL
ORDER BY
  total_clicks_count DESC
LIMIT
  100;