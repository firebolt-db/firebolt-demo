import os
import sys
import time
import logging
import json
from flask import Flask, jsonify, render_template, request
from shapely import wkt
from shapely.geometry import mapping
import osmnx as ox

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

# Set your Firebolt credentials from environment variables
client_id = os.getenv("FIREBOLT_CLIENT_ID", "")
client_secret = os.getenv("FIREBOLT_CLIENT_SECRET", "")
engine_name = os.getenv("FIREBOLT_ENGINE_NAME", "")
database_name = os.getenv("FIREBOLT_DATABASE", "")
account_name = os.getenv("FIREBOLT_ACCOUNT", "")

# Hardcoded locations as a fallback (if any)
location_polygons = {}

def connect_to_firebolt():
    credentials = ClientCredentials(client_id=client_id, client_secret=client_secret)
    connection = connect(
        engine_name=engine_name,
        database=database_name,
        account_name=account_name,
        auth=credentials,
    )
    return connection

app = Flask(__name__)
app.config["MAPBOX_TOKEN"] = MAPBOX_TOKEN  # pass token to templates

def build_query(location, severity, start_date, end_date):
    polygon_wkt = location_polygons.get(location)
    if not polygon_wkt:
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
        polygon_wkt = geom.wkt

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

@app.route('/geojson')
def get_geojson():
    location = request.args.get("location", "Long Beach")
    severity = request.args.get("severity", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()

    try:
        query = build_query(location, severity, start_date, end_date)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    connection = None
    try:
        connection = connect_to_firebolt()
        cursor = connection.cursor()
        start_time = time.time()
        cursor.execute(query)
        rows = cursor.fetchall()
        elapsed_time = time.time() - start_time
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
        data_scanned = cursor.rowcount if cursor.rowcount is not None else "N/A"

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
    finally:
        if connection:
            try:
                connection.close()
            except Exception:
                pass

@app.route('/')
def index():
    return render_template('index.html', locations=list(location_polygons.keys()))

if __name__ == '__main__':
    app.run(debug=True)
