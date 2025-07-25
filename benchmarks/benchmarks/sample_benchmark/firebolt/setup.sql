-- Example setup SQL
CREATE TABLE IF NOT EXISTS test_table (
    id INT,
    value STRING
)
PRIMARY INDEX id;

INSERT INTO test_table (id, value) VALUES (1, 'test');