-- Load NYC Parking Violations data from S3
-- Data source: Firebolt public sample datasets

-- First, let's check if we can connect and see the current state
SELECT 'Starting data load...' as status;

-- Load data from S3 parquet files
-- This will automatically create the table structure if needed
COPY INTO violations FROM 's3://firebolt-sample-datasets-public-us-east-1/nyc_sample_datasets/nycparking/parquet/'
WITH PATTERN="*.parquet" 
AUTO_CREATE=TRUE 
TYPE=PARQUET;

-- Verify the data was loaded
SELECT 
    COUNT(*) as total_rows,
    MIN(issue_date) as earliest_date,
    MAX(issue_date) as latest_date,
    COUNT(DISTINCT registration_state) as unique_states,
    COUNT(DISTINCT vehicle_make) as unique_makes,
    SUM(fine_amount) as total_fines
FROM violations;

-- Show sample data
SELECT 
    summons_number,
    plate_id,
    registration_state,
    issue_date,
    violation_code,
    vehicle_make,
    street_name,
    fine_amount
FROM violations 
ORDER BY issue_date DESC 
LIMIT 10;

-- Create some basic statistics
SELECT 'Data load completed successfully!' as status; 