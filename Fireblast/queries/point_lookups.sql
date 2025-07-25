-- Point Lookup Query 1: Single Record by Primary Key
SELECT 
    id, 
    ltv_date, 
    app_id, 
    media_source, 
    attribution_type,
    clicks_count, 
    impressions_count, 
    installs_count
FROM dml_test 
WHERE id = 12345;

-- Point Lookup Query 2: App-specific Records for Recent Date
SELECT 
    id,
    media_source,
    attribution_type,
    clicks_count,
    impressions_count,
    installs_count,
    inappevents_count,
    launches_count
FROM dml_test 
WHERE app_id = 'com.example.testapp' 
  AND ltv_date = CURRENT_DATE - INTERVAL '1 day'
ORDER BY clicks_count DESC
LIMIT 10;

-- Point Lookup Query 3: Media Source Specific Lookup
SELECT 
    app_id,
    ltv_date,
    clicks_count,
    impressions_count,
    installs_count
FROM dml_test 
WHERE media_source = 'facebook' 
  AND attribution_type = 'click'
  AND ltv_date BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
ORDER BY ltv_date DESC, clicks_count DESC
LIMIT 50;

-- Point Lookup Query 4: High-Performance Records
SELECT 
    id,
    app_id,
    ltv_date,
    media_source,
    clicks_count,
    installs_count
FROM dml_test 
WHERE clicks_count > 100 
  AND installs_count > 10
  AND ltv_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY installs_count DESC
LIMIT 25; 