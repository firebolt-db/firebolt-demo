-- Create the main violations table for NYC Parking Violations data
-- Schema based on NYC Open Data: Parking Violations Issued – Fiscal Year 2019-2023

DROP TABLE IF EXISTS violations;

CREATE TABLE violations (
    summons_number BIGINT,
    plate_id STRING,
    registration_state STRING,
    plate_type STRING,
    issue_date DATE,
    violation_code INT,
    vehicle_body_type STRING,
    vehicle_make STRING,
    issuing_agency STRING,
    street_code1 INT,
    street_code2 INT,
    street_code3 INT,
    vehicle_expiration_date DATE,
    violation_location STRING,
    violation_precinct INT,
    issuer_precinct INT,
    issuer_code INT,
    issuer_command STRING,
    issuer_squad STRING,
    violation_time STRING,
    time_first_observed STRING,
    violation_county STRING,
    violation_in_front_of_or_opposite STRING,
    house_number STRING,
    street_name STRING,
    intersecting_street STRING,
    date_first_observed DATE,
    law_section INT,
    sub_division STRING,
    violation_legal_code STRING,
    days_parking_in_effect STRING,
    from_hours_in_effect STRING,
    to_hours_in_effect STRING,
    vehicle_color STRING,
    unregistered_vehicle STRING,
    vehicle_year INT,
    meter_number STRING,
    feet_from_curb INT,
    violation_post_code STRING,
    violation_description STRING,
    no_standing_or_stopping_violation STRING,
    hydrant_violation STRING,
    double_parking_violation STRING,
    latitude DOUBLE,
    longitude DOUBLE,
    community_board INT,
    community_council INT,
    census_tract INT,
    bin INT,
    bbl BIGINT,
    nta STRING,
    fine_amount DOUBLE
) PRIMARY INDEX summons_number;

-- Create a summary table for aggregated data
DROP TABLE IF EXISTS violation_summary;

CREATE TABLE violation_summary (
    violation_date DATE,
    total_violations INT,
    total_fine_amount DOUBLE,
    avg_fine_amount DOUBLE,
    top_violation_code INT,
    top_street STRING
) PRIMARY INDEX violation_date; 