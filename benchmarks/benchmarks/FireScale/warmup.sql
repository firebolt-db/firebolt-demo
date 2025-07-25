-- General warmup queries for FireScale benchmark
-- These queries ensure all tables are cached for fair performance comparison
SELECT COUNT(*) FROM uservisits;
SELECT COUNT(*) FROM rankings;
SELECT COUNT(*) FROM agents; 
SELECT COUNT(*) FROM ipaddresses;
SELECT COUNT(*) FROM searchwords;