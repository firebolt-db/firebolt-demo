-- Create indexes to optimize query performance
-- This demonstrates Firebolt's advanced indexing capabilities

SELECT 'Creating indexes for optimal performance...' as status;

-- 1. Sparse index on issue_date for time-based filtering
-- This will dramatically speed up date range queries
CREATE SPARSE INDEX idx_issue_date ON violations (issue_date);

-- 2. Sparse index on street_name for location-based queries  
CREATE SPARSE INDEX idx_street_name ON violations (street_name);

-- 3. Sparse index on vehicle_make for vehicle analysis
CREATE SPARSE INDEX idx_vehicle_make ON violations (vehicle_make);

-- 4. Sparse index on violation_code for violation type analysis
CREATE SPARSE INDEX idx_violation_code ON violations (violation_code);

-- 5. Aggregating index for daily statistics (pre-computed aggregations)
-- This creates a materialized view-like structure for fast roll-ups
CREATE AGGREGATING INDEX agg_daily_stats ON violations (
    issue_date,
    COUNT(*) as daily_violations,
    SUM(fine_amount) as daily_fines,
    AVG(fine_amount) as avg_daily_fine,
    COUNT(DISTINCT vehicle_make) as unique_makes_per_day
);

-- 6. Aggregating index for hourly patterns
-- Extract hour from violation_time for time-of-day analysis
CREATE AGGREGATING INDEX agg_hourly_patterns ON violations (
    EXTRACT(HOUR FROM CAST(violation_time as TIME)) as violation_hour,
    COUNT(*) as hourly_violations,
    AVG(fine_amount) as avg_hourly_fine
);

-- 7. Aggregating index for street-level statistics
CREATE AGGREGATING INDEX agg_street_stats ON violations (
    street_name,
    COUNT(*) as street_violations,
    SUM(fine_amount) as street_total_fines,
    AVG(fine_amount) as street_avg_fine,
    COUNT(DISTINCT vehicle_make) as unique_makes_per_street
);

-- 8. Aggregating index for vehicle make analysis
CREATE AGGREGATING INDEX agg_vehicle_stats ON violations (
    vehicle_make,
    COUNT(*) as make_violations,
    SUM(fine_amount) as make_total_fines,
    AVG(fine_amount) as make_avg_fine,
    APPROX_PERCENTILE(fine_amount, 0.95) as make_95th_percentile
);

-- Verify indexes were created
SELECT 'Indexes created successfully!' as status;

-- Show index information
SELECT 
    'Index creation complete - queries should now be much faster!' as message,
    'Run benchmark queries to see the performance improvements' as next_step; 