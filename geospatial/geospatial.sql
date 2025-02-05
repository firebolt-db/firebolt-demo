-- Create an external table directly on CSV data from Kaggle
-- The data is publicly hosted in S3 by Firebolt
CREATE external TABLE accidentdata_ext (
  id TEXT NULL,
  source TEXT NULL,
  severity BIGINT NULL,
  start_time TIMESTAMP NULL,
  end_time TIMESTAMP NULL,
  start_lat DOUBLE PRECISION NULL,
  start_lng DOUBLE PRECISION NULL,
  end_lat DOUBLE PRECISION NULL,
  end_lng DOUBLE PRECISION NULL,
  distance_mi DOUBLE PRECISION NULL,
  description TEXT NULL,
  street TEXT NULL,
  city TEXT NULL,
  county TEXT NULL,
  state TEXT NULL,
  zipcode TEXT NULL,
  country TEXT NULL,
  timezone TEXT NULL,
  airport_code TEXT NULL,
  weather_timestamp TIMESTAMP NULL,
  temperature_f DOUBLE PRECISION NULL,
  wind_chill_f DOUBLE PRECISION NULL,
  humidity_percentage DOUBLE PRECISION NULL,
  pressure_in DOUBLE PRECISION NULL,
  visibility_mi DOUBLE PRECISION NULL,
  wind_direction TEXT NULL,
  wind_speed_mph DOUBLE PRECISION NULL,
  precipitation_in DOUBLE PRECISION NULL,
  weather_condition TEXT NULL,
  amenity BOOLEAN NULL,
  bump BOOLEAN NULL,
  crossing BOOLEAN NULL,
  give_way BOOLEAN NULL,
  junction BOOLEAN NULL,
  no_exit BOOLEAN NULL,
  railway BOOLEAN NULL,
  roundabout BOOLEAN NULL,
  station BOOLEAN NULL,
  stop BOOLEAN NULL,
  traffic_calming BOOLEAN NULL,
  traffic_signal BOOLEAN NULL,
  turning_loop BOOLEAN NULL,
  sunrise_sunset TEXT NULL,
  civil_twilight TEXT NULL,
  nautical_twilight TEXT NULL,
  astronomical_twilight TEXT NULL
) URL = 's3://firebolt-sample-datasets-public-us-east-1/us-accidents-data/' 
  OBJECT_PATTERN = '*.csv' TYPE = (CSV SKIP_HEADER_ROWS = TRUE ALLOW_SINGLE_QUOTES = False)

/** 
* There's now two possible strategies to create our table in Firebolt
* 
* The first is to manually select all columns and explicitly transform the longitude and latitude
* data to geospatial points using the ST_GeogPoint() function. This has the benefit of preserving
* the order of the columns.
*
* The second is to select all columns with SELECT * and use the ST_GeogPoint() function at the end.
* This reduces verbosity, but the geography columns will be moved to the end of the table.
*/

-- CTAS option 1 (if you care about the order of the columns)  
create table accidentdata as
select
  id,
  source,
  severity,
  start_time,
  end_time,
  ST_GeogPoint (start_lng, start_lat) AS start_location,
  ST_GeogPoint (end_lng, end_lat) AS end_location,
  distance_mi,
  description,
  street,
  city,
  county,
  state,
  zipcode,
  country,
  timezone,
  airport_code,
  weather_timestamp,
  temperature_f,
  wind_chill_f,
  humidity_percentage,
  pressure_in,
  visibility_mi,
  wind_direction,
  wind_speed_mph,
  precipitation_in,
  weather_condition,
  amenity,
  bump,
  crossing,
  give_way,
  junction,
  no_exit,
  railway,
  roundabout,
  station,
  stop,
  traffic_calming,
  traffic_signal,
  turning_loop,
  sunrise_sunset,
  civil_twilight,
  nautical_twilight,
  astronomical_twilight
from
  accidentdata_ext

-- CTAS option 2 (less verbose, but the Geo columns will be at the end)  
create table accidentdata as
select
  * exclude(start_lat, start_lng, end_lat, end_lng),
  ST_GeogPoint (start_lng, start_lat) AS start_location,
  ST_GeogPoint (end_lng, end_lat) AS end_location,
from
  accidentdata_ext

-- Let's check the number of rows from our table to confirm full ingestion
select count(*) from accidentdata
--7,728,394
select count(*) from accidentdata_ext
--7,728,394

/* Ok, so now we have the data and everything setup correctly, let’s begin! */
-- 1. Let’s define a Polygon for Central Park. 
-- In this query, we show a polygon representing the Central Park area in New York City, defined using WKT (Well-Known Text) format.

set query_parameters={"name":"central_park","value":"POLYGON((-73.95826578140259 40.80120581546623,-73.94845962524414 40.79711243898632,-73.97289991378783 40.76401504612403,-73.98268461227417 40.76785044388771,-73.95826578140259 40.80120581546623))"};

-- 2. Now, Let’s Count Accidents by Year Within Central Park
-- This query calculates the number of accidents occurring inside Central Park for each year. 

select extract(year from start_time) as year, count(*)
from accidentdata
where   
  st_covers(st_geogfromtext(param('central_park')), start_location)
group by all
order by year;

-- 3. Next, Let’s Retrieve Accident Points Within Central Park
-- This query extracts the geographic coordinates of all accidents that occurred within Central Park.
select st_astext(start_location) 
from accidentdata
where st_covers(st_geogfromtext(param('central_park')), start_location);

-- 4.  Let’s Try a New Scenario and Find Where Most of the Accidents Happen in US
-- Output of the query gives us S2 cell id: -9168534571950538752
-- This query groups accident data by S2 cells at level 15, a spatial granularity that divides Earth's surface into cells of approximately 79173 m² - about the size of 9-10 soccer fields

SELECT 
    ST_S2CellIdFromPoint(start_location, 15) AS s2_cell_id, 
    COUNT(*) AS c
FROM 
    accidentdata
GROUP BY 
    s2_cell_id
ORDER BY 
    c DESC
LIMIT 1;

-- 5. Now, Let’s Find ALL Accidents at the above Cell ID: -9168534571950538752
-- Output -> South LA
SELECT st_astext(start_location) AS geometry_wkt
FROM accidentdata
WHERE st_s2cellidfrompoint(start_location, 15) = -9168534571950538752;