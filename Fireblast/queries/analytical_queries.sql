-- Analytical Query 1: Conversion Funnel Analysis
WITH funnel_data AS (
    SELECT 
        app_id,
        media_source,
        SUM(impressions_count) as total_impressions,
        SUM(clicks_count) as total_clicks,
        SUM(installs_count) as total_installs,
        SUM(inappevents_count) as total_events
    FROM dml_test 
    WHERE ltv_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY app_id, media_source
)
SELECT 
    app_id,
    media_source,
    total_impressions,
    total_clicks,
    total_installs,
    total_events,
    CASE WHEN total_impressions > 0 
         THEN ROUND(total_clicks * 100.0 / total_impressions, 2) 
         ELSE 0 END as ctr_pct,
    CASE WHEN total_clicks > 0 
         THEN ROUND(total_installs * 100.0 / total_clicks, 2) 
         ELSE 0 END as install_rate_pct,
    CASE WHEN total_installs > 0 
         THEN ROUND(total_events * 1.0 / total_installs, 2) 
         ELSE 0 END as events_per_install
FROM funnel_data
WHERE total_impressions > 1000
ORDER BY total_installs DESC
LIMIT 100;

-- Analytical Query 2: Cohort Performance Analysis
SELECT 
    DATE_TRUNC('week', ltv_date) as week_start,
    media_source,
    COUNT(DISTINCT app_id) as unique_apps,
    SUM(clicks_count) as weekly_clicks,
    SUM(installs_count) as weekly_installs,
    AVG(clicks_count) as avg_clicks_per_record,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY clicks_count) as median_clicks,
    PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY clicks_count) as p90_clicks
FROM dml_test 
WHERE ltv_date >= CURRENT_DATE - INTERVAL '12 weeks'
GROUP BY DATE_TRUNC('week', ltv_date), media_source
HAVING SUM(clicks_count) > 50
ORDER BY week_start DESC, weekly_installs DESC;

-- Analytical Query 3: App Performance Ranking
WITH app_metrics AS (
    SELECT 
        app_id,
        COUNT(*) as total_records,
        SUM(clicks_count) as total_clicks,
        SUM(installs_count) as total_installs,
        SUM(inappevents_count) as total_events,
        COUNT(DISTINCT media_source) as media_diversity,
        MAX(ltv_date) as last_activity_date,
        AVG(clicks_count) as avg_clicks
    FROM dml_test 
    WHERE ltv_date >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY app_id
),
ranked_apps AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY total_installs DESC) as install_rank,
        ROW_NUMBER() OVER (ORDER BY total_clicks DESC) as click_rank,
        ROW_NUMBER() OVER (ORDER BY avg_clicks DESC) as avg_click_rank
    FROM app_metrics
    WHERE total_records > 5
)
SELECT 
    app_id,
    total_records,
    total_clicks,
    total_installs,
    total_events,
    media_diversity,
    last_activity_date,
    ROUND(avg_clicks, 2) as avg_clicks,
    install_rank,
    click_rank,
    avg_click_rank,
    ROUND((install_rank + click_rank + avg_click_rank) / 3.0, 1) as overall_rank_score
FROM ranked_apps
ORDER BY overall_rank_score ASC
LIMIT 50; 