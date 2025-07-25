CREATE SCHEMA IF NOT EXISTS sample_dataset;

CREATE TABLE IF NOT EXISTS sample_dataset.test_table (
    id INT,
    value STRING
);

INSERT INTO sample_dataset.test_table (id, value) VALUES (1, 'test');