--create aggregating indexes

CREATE AGGREGATING INDEX idx_ltv ON ltv (
        ltv_timestamp_dt,
        app_id,
        media_source,
        ltv_country,
        attribution_type,
      SUM(clicks_count),
      SUM(impressions_count),
      SUM(inappevents_count),
      SUM(launches_count),
      SUM(installs_count),
      COUNT(DISTINCT "app_id"),
      SUM(CASE WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count  ELSE NULL END),
      SUM(CASE WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count  ELSE NULL END),
      SUM(CASE WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count  ELSE NULL END)
)
;

CREATE AGGREGATING INDEX idx_ltv_kpi ON ltv (
        ltv_timestamp_dt,
        media_source,
      SUM(clicks_count),
      SUM(impressions_count),
      SUM(inappevents_count),
      SUM(launches_count),
      SUM(installs_count),
      COUNT(DISTINCT "app_id"),
      SUM(CASE WHEN (ltv.attribution_type = 'install') THEN ltv.clicks_count  ELSE NULL END),
      SUM(CASE WHEN (ltv.attribution_type = 'install') THEN ltv.impressions_count  ELSE NULL END),
      SUM(CASE WHEN (ltv.attribution_type = 'install') THEN ltv.installs_count  ELSE NULL END)
)
;

