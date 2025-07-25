-- Aggregation Query 1: Daily App Metrics Summary
SELECT 
    ltv_date,
    app_id,
    COUNT(*) as record_count,
    SUM(clicks_count) as total_clicks,
    SUM(impressions_count) as total_impressions,
    SUM(installs_count) as total_installs,
    AVG(clicks_count) as avg_clicks
FROM dml_test 
WHERE ltv_date >= '2024-01-01'
GROUP BY ltv_date, app_id
ORDER BY ltv_date DESC, total_clicks DESC
LIMIT 100;

-- Aggregation Query 2: Media Source Performance Analysis
SELECT 
    media_source,
    attribution_type,
    COUNT(DISTINCT app_id) as unique_apps,
    SUM(clicks_count + impressions_count) as total_traffic,
    SUM(installs_count) as total_installs,
    CASE WHEN SUM(clicks_count) > 0 
         THEN ROUND(SUM(installs_count) * 100.0 / SUM(clicks_count), 2) 
         ELSE 0 END as install_rate_pct
FROM dml_test 
GROUP BY media_source, attribution_type
HAVING SUM(clicks_count) > 10
ORDER BY total_installs DESC;

-- Aggregation Query 3: Time-based Performance Metrics
SELECT 
    DATE_TRUNC('month', ltv_date) as month,
    SUM(clicks_count) as monthly_clicks,
    SUM(impressions_count) as monthly_impressions, 
    SUM(installs_count) as monthly_installs,
    SUM(inappevents_count) as monthly_events,
    COUNT(DISTINCT app_id) as active_apps
FROM dml_test
WHERE ltv_date >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY DATE_TRUNC('month', ltv_date)
ORDER BY month DESC; 