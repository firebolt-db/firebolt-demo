# Firebolt CDC Demo with Debezium & Kafka

## Overview

This demo showcases how you can use Debezium & Kafka to perform CDC to Firebolt based on 
data written to a local Postgres database. By configuring your source connector to any 
other system supported by Debezium, you can thus do CDC into Firebolt from a number of 
different platforms.

## Setup Instructions

### Step 1: Python Environment Setup

Ensure you have Python 3.8+ installed. Optionally, create a virtual environment using a 
tool like venv or uv.

Then install required packages:
```bash
/kafka-cdc$ pip install -r requirements.txt
```

### Step 2: Firebolt Configuration

Edit the file `sink-connector.json` and enter your Firebolt connection details.

```json
{
    "name": "firebolt-sink-connector",
    "config": {
        "connection.url": "jdbc:firebolt:<your Firebolt database>?account=<your Firebolt account>&engine=<your Firebolt engine>&merge_prepared_statement_batches=true",
        "connection.username": "<your Firebolt service account ID>",
        "connection.password": "<your Firebolt secret key>",
    }
}
```

Replace the values wrapped in `<carrots>` with the correct information:
* `<your Firebolt database>`: the name of the database to write to in Firebolt
* `<your Firebolt account>`: the name of the Firebolt account your database is in.
* `<your Firebolt engine>`: the name of the engine you'd like to use for writing into 
  Firebolt.
* `<your Firebolt service account ID>`: the account ID for the
  [service account](https://docs.firebolt.io/guides/managing-your-organization/service-accounts)
  you're using.
* `<your Firebolt secret key>`: the secret key for that service account.

When these options are configured, it should look like:

```json
{
    "name": "firebolt-sink-connector",
    "config": {
        "connection.url": "jdbc:firebolt:mydatabase?account=myaccount&engine=myengine&merge_prepared_statement_batches=true",
        "connection.username": "1234567890abc",
        "connection.password": "11aa22bb33cc44dd55ee66ff77gg88hh99ii00jj",
    }
}
```

Please note that the other configuration options provided in the file should remain, but 
do not need to be modified.

Also make sure not to commit credentials to version control.

### Step 3: Create Tables in Firebolt

In the Firebolt database you specified, you now need to create the tables you intend to 
write to. The schema should have parity with the schema in Postgres, but you can define 
primary indexes in Firebolt, as well as specify whether a table is a fact or dimension 
table if desired. Run the following SQL statements in the database you configured above:

```sql
CREATE TABLE IF NOT EXISTS cdc_public_users (
  id integer NOT NULL,
  first_name text NOT NULL,
  last_name text NOT NULL,
  gender text NULL,
  address text NULL
) PRIMARY INDEX id;```

```sql
CREATE TABLE IF NOT EXISTS cdc_public_scores (
  user_id INTEGER NOT NULL,
  level_id INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  score INTEGER NOT NULL
) PRIMARY INDEX user_id,
level_id,
created_at;
```

### Step 4: Start Services with Docker Compose

Start the services:
```shell
docker compose up
```

In a separate terminal window, run POST requests to create the required connections:
```shell
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @source-connector.json
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @sink-connector.json
```

You can verify the status of the connectors with:

```shell
curl -X GET http://localhost:8083/connectors/postgres-source-connector/status
curl -X GET http://localhost:8083/connectors/firebolt-sink-connector/status
```

## Run the Demo

With everything set up, you are all set to generate data in Postgres, which will then 
automatically be written to Firebolt.

### Step 1: Generate Data

Invoke the Python script to start generating and sending data:
```bash
/kafka-cdc$ python generate_data.py <records_generated_per_5s>
```

For example, if you wanted to create 100 user records every 5 seconds, you could run:
```bash
/kafka-cdc$ python generate_data.py 100
```

By default, the script will run until 100,000 user records and 800,000 scores
have been written. If you'd like to exit early, simply use `Ctrl+C` to stop the script.

### Step 2: Query Data in Firebolt

The data will be written to the tables you created in the correct database and account.
You can query this data to see the count of records being written:

```sql
SELECT
  (
    SELECT
      COUNT(*)
    FROM
      cdc_public_scores
  ) AS score_count,
  (
    SELECT
      COUNT(*)
    FROM
      cdc_public_users
  ) AS user_count;
```

You can also run analytical queries on the data:

```sql
SELECT
  user_id,
  first_name,
  last_name,
  score,
  created_at,
  address
FROM
  cdc_public_scores
  JOIN cdc_public_users ON user_id = id
WHERE
  level_id = 3
  AND address LIKE '%, WA%'
ORDER BY
  score DESC
LIMIT
  10;
```

Note that data is being generated by [Faker](https://faker.readthedocs.io/en/master/), 
and the example query provided above is searching for addresses in Washington state in 
the US. If you only have a small number of records written to Firebolt so far, it is 
possible that a randomly-generated record will not yet exist that matches the provided 
query. However, with a sufficient number of generated rows (1000+), it should always 
return results.

### Step 3: Explore!

With the schemas provided in this demo, there's far more queries you can write. This demo
is, for example, a great platform to test on `VACUUM` and auto-vacuum behavior in 
Firebolt.

If you'd like, you can connect to your locally-hosted Postgres directly in a terminal 
window with:
```shell
/kafka-cdc$ docker compose exec postgres psql -U demouser -d postgres
```

By default, the connectors have also been configured to listen to and write to a table
named `demo` in Postgres and `cdc_public_demo` in Firebolt. You can create this table
with the same schema in both locations, and data written to the Postgres table should be
synced to Firebolt.

You can also change the configuration of your connectors to add more tables, or modify 
the data generation script if you'd like to do things differently. If you change the 
configuration of either connector, you can re-create them by first deleting them:
```shell
curl -X DELETE http://localhost:8083/connectors/postgres-source-connector
curl -X DELETE http://localhost:8083/connectors/firebolt-sink-connector
```
Then re-create them as outlined above.

If you have any questions, feel free to open an issue in this repository, or reach out
to us on the [Firebolt Discord](https://discord.com/invite/UpMPDHActM).