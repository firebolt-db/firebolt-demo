import os
import sys
import time
import logging
import json
import queue
from flask import Flask, jsonify, render_template, request
from shapely import wkt
from shapely.geometry import mapping
import osmnx as ox
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import Firebolt client modules
from firebolt.client.auth import ClientCredentials
from firebolt.db import connect

# Read Mapbox token from file
with open("mapbox_token.txt") as f:
    MAPBOX_TOKEN = f.read().strip()

# Configure logging (file and console)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# File handler
fh = logging.FileHandler("firebolt_large_benchmark.log")
fh.setFormatter(formatter)
logger.addHandler(fh)
# Stream handler (console)
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)

# -----------------------------
# Firebolt Credentials
# -----------------------------
client_id = os.getenv("FIREBOLT_CLIENT_ID", "")
client_secret = os.getenv("FIREBOLT_CLIENT_SECRET", "")
engine_name = os.getenv("FIREBOLT_ENGINE_NAME", "")
database_name = os.getenv("FIREBOLT_DATABASE", "")
account_name = os.getenv("FIREBOLT_ACCOUNT", "")

if not account_name:
    logger.error("FIREBOLT_ACCOUNT environment variable is not set!")
    raise Exception("FIREBOLT_ACCOUNT environment variable must be set!")

def connect_to_firebolt():
    credentials = ClientCredentials(client_id=client_id, client_secret=client_secret)
    connection = connect(
        engine_name=engine_name,
        database=database_name,
        account_name=account_name,
        auth=credentials,
    )
    return connection

def build_query(location, severity, start_date, end_date):
    # Always perform geocoding to get the polygon in WKT format.
    try:
        gdf = ox.geocode_to_gdf(location)
    except Exception as e:
        logger.error(f"Geocoding error for '{location}': {str(e)}")
        raise Exception(f"Geocoding error: {str(e)}")
    if gdf.empty:
        raise Exception(f"Location '{location}' not found")
    
    geom = gdf.iloc[0].geometry
    if geom.geom_type == "Point":
        geom = geom.buffer(0.01)
    polygon_wkt = geom.wkt  # Get the WKT representation.

    query = f"""
    SELECT DISTINCT
           id,
           severity,
           start_time,
           description,
           weather_condition,
           distance_mi,
           ST_AsText(start_location) AS location_wkt
    FROM accidentdata 
    WHERE ST_Contains(
         ST_GeogFromText('{polygon_wkt}'),
         start_location
    )
    """
    if severity:
        query += f"\nAND severity = '{severity}'"
    if start_date:
        query += f"\nAND to_date(start_time) >= '{start_date}'"
    if end_date:
        query += f"\nAND to_date(start_time) <= '{end_date}'"
    query += ";"
    return query

# -----------------------------
# Connection Pool Classes
# -----------------------------
class FireboltConnectionPool:
    def __init__(self, pool_size):
        self.pool = queue.Queue(maxsize=pool_size)
        self.pool_size = pool_size
        self.initialize_pool()

    def initialize_pool(self):
        for _ in range(self.pool_size):
            conn = connect_to_firebolt()
            self.pool.put(conn)

    def get_connection(self, timeout=None):
        try:
            return self.pool.get(timeout=timeout)
        except queue.Empty:
            raise Exception("No available connection in the pool.")

    def return_connection(self, conn):
        try:
            self.pool.put(conn, block=False)
        except queue.Full:
            conn.close()

    def close_all(self):
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()

class FireboltConnectionPoolSmart(FireboltConnectionPool):
    """
    Smart connection pool that executes the query and only replaces
    the connection if the query fails. Uses a persistent cursor per connection.
    """
    def execute_query(self, query, timeout=10):
        conn = self.get_connection(timeout=timeout)
        try:
            # Use persistent cursor: if it doesn't exist, create it once.
            if not hasattr(conn, '_persistent_cursor'):
                conn._persistent_cursor = conn.cursor()
            cursor = conn._persistent_cursor
            start_time = time.time()
            cursor.execute(query)
            rows = cursor.fetchall()
            elapsed_time = time.time() - start_time
            # Do NOT close the persistent cursor so it can be reused.
            self.return_connection(conn)
            return rows, elapsed_time
        except Exception as e:
            logger.error(f"Query execution failed, replacing connection: {e}")
            try:
                conn.close()
            except Exception as e2:
                logger.error(f"Error closing faulty connection: {e2}")
            # Replace the bad connection with a new one.
            new_conn = connect_to_firebolt()
            self.return_connection(new_conn)
            raise e

POOL_SIZE = 5
connection_pool = FireboltConnectionPoolSmart(POOL_SIZE)

app = Flask(__name__)
app.config["MAPBOX_TOKEN"] = MAPBOX_TOKEN

@app.route('/geojson')
def get_geojson():
    location = request.args.get("location", "Long Beach")
    severity = request.args.get("severity", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()

    try:
        query = build_query(location, severity, start_date, end_date)
        logger.info(f"Executing Query:\n{query}")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        # Use the smart pool's execute_query method with the persistent cursor.
        start_time = time.time()
        rows, elapsed_time = connection_pool.execute_query(query)
        logger.info(f"Query executed in {elapsed_time:.4f} seconds for location: {location}")

        if not rows:
            return jsonify({"error": "No data found"}), 404

        features = []
        for row in rows:
            try:
                geom = wkt.loads(row[6])
            except Exception as ex:
                logger.error(f"Error parsing WKT: {row[6]} - {ex}")
                continue
            feature = {
                "type": "Feature",
                "geometry": mapping(geom),
                "properties": {
                    "id": row[0],
                    "severity": row[1],
                    "start_time": row[2],
                    "description": row[3],
                    "weather_condition": row[4],
                    "distance_mi": row[5]
                }
            }
            features.append(feature)
        geojson_obj = {
            "type": "FeatureCollection",
            "features": features
        }
        accident_count = len(features)
        data_scanned = accident_count

        response = {
            "geojson": geojson_obj,
            "query": query,
            "query_time": round(elapsed_time, 4),
            "data_scanned": data_scanned,
            "accident_count": accident_count
        }
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html', locations=[])

if __name__ == '__main__':
    app.run(debug=True)
