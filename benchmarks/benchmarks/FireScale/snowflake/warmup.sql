-- Warmup queries for Snowflake to ensure all tables are cached
SELECT COUNT(*) FROM uservisits;
SELECT COUNT(*) FROM rankings;
SELECT COUNT(*) FROM agents; 
SELECT COUNT(*) FROM ipaddresses;
SELECT COUNT(*) FROM searchwords;