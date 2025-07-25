-- Sample SQL queries for testing
-- These queries are used in unit and integration tests

-- Query 1: Simple select with literal
SELECT 1 AS test_column, 'test_value' AS test_string;

-- Query 2: Basic aggregation
SELECT 
    COUNT(*) as total_rows,
    AVG(id) as avg_id,
    MAX(created_date) as latest_date
FROM test_table;

-- Query 3: Join with filtering
SELECT 
    u.id,
    u.name,
    p.title as profile_title
FROM users u
JOIN user_profiles p ON u.id = p.user_id  
WHERE u.active = true
AND u.created_date >= '2024-01-01';

-- Query 4: Window function
SELECT 
    id,
    name,
    created_date,
    ROW_NUMBER() OVER (ORDER BY created_date DESC) as row_num
FROM users
WHERE active = true;

-- Query 5: Complex query with subquery
SELECT 
    category,
    COUNT(*) as item_count,
    AVG(price) as avg_price
FROM products 
WHERE category IN (
    SELECT category 
    FROM product_categories 
    WHERE active = true
)
GROUP BY category
HAVING COUNT(*) > 5
ORDER BY avg_price DESC;