SET
  warmup = true;


--1
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-28')
    )
  )
  AND ltv.media_source = '3bc36bb9f1bded2703684dae170581dc'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--2
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-15')
    )
  )
  AND ltv.media_source = '3bc36bb9f1bded2703684dae170581dc'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--3
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-28')
    )
  )
  AND ltv.media_source = 'e391b3d1930968f4cce0d5dee539d256'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--4
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-15')
    )
  )
  AND ltv.media_source = 'e391b3d1930968f4cce0d5dee539d256'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--5
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-28')
    )
  )
  AND ltv.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--6
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-15')
    )
  )
  AND ltv.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--7
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-28')
    )
  )
  --AND ltv.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--8
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-15')
    )
  )
  -- AND ltv.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--9
SELECT
  count(*)
FROM
  (
    SELECT
      (
        (
          CASE
            WHEN t0.__meASure__0 = 0 THEN NULL
            ELSE CAST(installs_count AS DOUBLE PRECISION) / t0.__meASure__0
          END
        ) * 10000
      ) AS Calculation_152348354691211271,
      SOURCE_FILE_NAME,
      SOURCE_FILE_TIMESTAMP,
      acc_name,
      ad,
      ad_id,
      adset_id,
      adset_name,
      app_id,
      app_name,
      app_slug,
      attributed_touch_type,
      attribution_type,
      campaign,
      campaign_id,
      channel,
      click_installs_count,
      clicks_count,
      currency,
      dAShboard_device_rank,
      event_name,
      first_inapps,
      impression_installs_count,
      impressions_count,
      inappevents_count,
      install_ASsists,
      install_cost,
      install_cost_alt,
      installs_count,
      is_attributed,
      keywords,
      launches_count,
      loyals,
      ltv_country,
      ltv_currency,
      ltv_device_rank,
      ltv_hour_tz,
      ltv_timestamp,
      ltv_timestamp_dt,
      ltv_timezone,
      custom_sql_query.media_source,
      organic_first_inapps,
      organic_inappevents_count,
      organic_installs_count,
      organic_launches_count,
      organic_loyals,
      organic_revenue,
      organic_revenue_alt,
      owner_account,
      partner,
      platform,
      region,
      revenue,
      revenue_alt,
      shipping_country,
      site_id,
      source,
      uninstalls_count,
      unmASked_media_source
    FROM
      (
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
          ltv
          LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
          LEFT JOIN account AS acc ON acc.id = app.owner_account
      ) custom_sql_query
      INNER JOIN (
        SELECT
          SUM(installs_count) AS __meASure__0,
          media_source
        FROM
          (
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
              ltv
              LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
              LEFT JOIN account AS acc ON acc.id = app.owner_account
          ) custom_sql_query
        GROUP BY
          2
      ) t0 ON (custom_sql_query.media_source = t0.media_source)
    WHERE
      (
        (ltv_timestamp_dt >= (DATE '2025-02-01'))
        AND (ltv_timestamp_dt <= (DATE '2025-02-28'))
        AND (
          custom_sql_query.media_source = 'e391b3d1930968f4cce0d5dee539d256'
          OR custom_sql_query.media_source = '3bc36bb9f1bded2703684dae170581dc'
          OR custom_sql_query.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
        )
      )
  ) AS a;


--10
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-28')
    )
  )
  AND ltv.media_source = '3bc36bb9f1bded2703684dae170581dc'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--11
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-15')
    )
  )
  AND ltv.media_source = '3bc36bb9f1bded2703684dae170581dc'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--12
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-28')
    )
  )
  AND ltv.media_source = 'e391b3d1930968f4cce0d5dee539d256'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--13
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-15')
    )
  )
  AND ltv.media_source = 'e391b3d1930968f4cce0d5dee539d256'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--14
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-28')
    )
  )
  AND ltv.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--15
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-15')
    )
  )
  AND ltv.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--16
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-28')
    )
  )
  --AND ltv.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--17
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
      ltv
      LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
      LEFT JOIN account AS acc ON acc.id = app.owner_account
  )
SELECT
  ltv.app_name,
  ltv.media_source,
  ltv.acc_name,
  ltv.shipping_country,
  ltv.region,
  ltv.platform,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count
        ELSE NULL
      END
    ),
    0
  ) AS total_clicks_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count
        ELSE NULL
      END
    ),
    0
  ) AS total_impressions_count,
  COALESCE(SUM(ltv.inappevents_count), 0) AS total_inappevents_count,
  COALESCE(SUM(ltv.launches_count), 0) AS total_launches_count,
  COALESCE(
    SUM(
      CASE
        WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count
        ELSE NULL
      END
    ),
    0
  ) AS total_noi_count
FROM
  ltv
WHERE
  (
    (
      (ltv.ltv_timestamp_dt) >= (TIMESTAMP '2025-02-01')
      AND (ltv.ltv_timestamp_dt) < (TIMESTAMP '2025-02-15')
    )
  )
  -- AND ltv.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
GROUP BY ALL
ORDER BY
  7 DESC
LIMIT
  100;


--18
SELECT
  count(*)
FROM
  (
    SELECT
      (
        (
          CASE
            WHEN t0.__meASure__0 = 0 THEN NULL
            ELSE CAST(installs_count AS DOUBLE PRECISION) / t0.__meASure__0
          END
        ) * 10000
      ) AS Calculation_152348354691211271,
      SOURCE_FILE_NAME,
      SOURCE_FILE_TIMESTAMP,
      acc_name,
      ad,
      ad_id,
      adset_id,
      adset_name,
      app_id,
      app_name,
      app_slug,
      attributed_touch_type,
      attribution_type,
      campaign,
      campaign_id,
      channel,
      click_installs_count,
      clicks_count,
      currency,
      dAShboard_device_rank,
      event_name,
      first_inapps,
      impression_installs_count,
      impressions_count,
      inappevents_count,
      install_ASsists,
      install_cost,
      install_cost_alt,
      installs_count,
      is_attributed,
      keywords,
      launches_count,
      loyals,
      ltv_country,
      ltv_currency,
      ltv_device_rank,
      ltv_hour_tz,
      ltv_timestamp,
      ltv_timestamp_dt,
      ltv_timezone,
      custom_sql_query.media_source,
      organic_first_inapps,
      organic_inappevents_count,
      organic_installs_count,
      organic_launches_count,
      organic_loyals,
      organic_revenue,
      organic_revenue_alt,
      owner_account,
      partner,
      platform,
      region,
      revenue,
      revenue_alt,
      shipping_country,
      site_id,
      source,
      uninstalls_count,
      unmASked_media_source
    FROM
      (
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
          ltv
          LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
          LEFT JOIN account AS acc ON acc.id = app.owner_account
      ) custom_sql_query
      INNER JOIN (
        SELECT
          SUM(installs_count) AS __meASure__0,
          media_source
        FROM
          (
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
              ltv
              LEFT JOIN owned_apps AS app ON ltv.app_id = app.app_slug
              LEFT JOIN account AS acc ON acc.id = app.owner_account
          ) custom_sql_query
        GROUP BY
          2
      ) t0 ON (custom_sql_query.media_source = t0.media_source)
    WHERE
      (
        (ltv_timestamp_dt >= (DATE '2025-02-01'))
        AND (ltv_timestamp_dt <= (DATE '2025-02-28'))
        AND (
          custom_sql_query.media_source = 'e391b3d1930968f4cce0d5dee539d256'
          OR custom_sql_query.media_source = '3bc36bb9f1bded2703684dae170581dc'
          OR custom_sql_query.media_source = 'b935fcce8f277b6c60cd7598349c64e8'
        )
      )
  ) AS a;


SET
  warmup = false;