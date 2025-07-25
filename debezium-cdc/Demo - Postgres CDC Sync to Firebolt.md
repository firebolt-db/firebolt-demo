### Background:
- this demo showcases the integration between **Postgres** and **Firebolt** using **Debezium** for real-time change data capture (CDC)
- the use case simulates syncing real-time transactional data from Postgres to Firebolt for analytical purposes
### Prerequisites:
- refer to documentation: [debezium with firebolt](https://docs.firebolt.io/Guides/integrations/debezium.html)
- In Firebolt use:
	- account: se-demo-account
	- engine: debezium_ingestion & debezium_analytics
	- database: demo_debezium_cdc
- Outside Firebolt Prerequisites:
	- install [Firebolt JDBC Driver](https://github.com/firebolt-db/jdbc/releases)
	- install [Docker](https://docs.docker.com/get-started/get-docker/)
	- `firebolt-sink-connector.json`
	- `docker-compose.yml` (**update volumes section with correct path to jar**)
	- `source-connector.json`
### Set-Up Steps:
- run `docker compose up` in the directory containing `docker-compose.yml` file
- make a POST request to set up a source connector with the config file `source-connector.json` set up earlier:
```
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @source-connector.json
```

- make a POST request to set up a sink connector with the config file `firebolt-sink-connector.json` set up earlier:
```
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @firebolt-sink-connector.json
```

- verify the status of the connectors:
```
curl -X GET http://localhost:8083/connectors/postgres-source-connector/status
curl -X GET http://localhost:8083/connectors/firebolt-sink-connector/status
```
![[Pasted image 20250512132040.png]]

- node insert_fake_data.js 


### Running Demo:
- explain the situation:
	- your application is writing transactional data to Postgres, and this data needs to be synced with Firebolt for analytical queries
- questions to ask:
	- how often is data being written to postgres?
	- how much data is being processed during the sync?
	- what are the end-users' SLA requirements on analyzing the latest data?
	- 
1. start in Firebolt:
	- run the query: `select count(*) from cdc_public_demo;` 
	- show that currently there are 0 rows in this table
	- ![[Pasted image 20250512162708.png]]
2. switch to terminal:
	node ingest_data.js 

```

3. switch to streamlit:
	- show live data streaming in

### Other Things:
- Firebolt currently does not support certain CDC scenarios (not sure when this will be supported):
	- You can only insert or update data in your table using either `insert` or `update` mode. The `"insert.mode":"upsert"` setting is not yet supported.
	- Append+Update and CDC scenarios are not yet supported due to the limitation above