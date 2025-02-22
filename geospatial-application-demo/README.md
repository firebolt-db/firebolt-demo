# Firebolt Map Analytics Demo

This project is a demonstration of Firebolt’s speed for geospatial analytics on an interactive Mapbox map. The application dynamically queries a Firebolt database to display accident data in real time and showcases various map visualization modes and filtering options.

## Features

- **Interactive Map Visualization**
  - Displays accident data on a Mapbox map.
  - Two visualization modes:
    - **Clustered View:** Groups accident points.
    - **Heatmap View:** Shows a color-coded heatmap based on accident density and severity.
  - Accident points are styled by severity; clicking a point displays detailed information (ID, severity, start time, weather conditions, distance, and description).
  - Map style switcher allows users to choose among Streets, Dark, Light, and Satellite base maps.

- **Dynamic Querying & Filters**
  - **Location Search:** Use Mapbox Geocoder to search for a location. If no pre-defined polygon exists, the app uses osmnx to generate a polygon for the location.
  - **Severity Filter:** Select accident severity from a dropdown.
  - **Year Range Sliders:** Adjust the start and end year with intuitive sliders.
  - Query information—including the generated SQL query, query execution time, and data scanned—is displayed in the Query Info panel.
  - An **Engine Status** message in the Query Info panel shows real-time feedback (e.g., “Engine starting…”, “Engine ready”, or “No results found”).

- **Connection Pooling (Optional)**
  - The backend uses a simple connection pool to reuse Firebolt connections, reducing connection overhead and improving performance.

- **Modular & Portable Code**
  - The project is organized into separate files for the Flask backend, HTML templates, CSS, and JavaScript.
  - The Mapbox access token is stored securely in a file (or loaded via environment variables) so it isn’t exposed directly in client-side code.

## Project Structure

```
firebolt-demo/
├── app.py                 # Main Flask application
├── mapbox_token.txt       # Contains your Mapbox public token (starting with "pk.")
├── requirements.txt       # List of Python dependencies
├── .env                   # (Optional) Environment variables for Firebolt credentials
├── static/
│   ├── css/
│   │   └── style.css      # Custom CSS styles
│   └── js/
│       └── app.js         # Custom JavaScript for map interaction
└── templates/
    └── index.html         # Main HTML template
```

## How It Works

1. **Location & Geocoding:**  
   - Users search for a location using the integrated Mapbox Geocoder.
   - If no pre-defined polygon exists, osmnx generates a polygon from the searched location.
   - This polygon is used to filter accident data in Firebolt.

2. **Dynamic Querying:**  
   - Based on the chosen location and filters (severity and year range), the app builds a dynamic SQL query.
   - The query is executed on Firebolt, which returns accident data in GeoJSON format.

3. **Map Visualization:**  
   - The GeoJSON data is rendered on a Mapbox map.
   - Users can switch between clustered and heatmap views.
   - Individual accident points are styled by severity; clicking a point shows detailed popups.

4. **Query Metrics & Engine Status:**  
   - The Query Info panel (bottom left) displays:
     - The generated SQL query.
     - Query execution time.
     - Data scanned (or accident count).
     - An engine status message (e.g., “Engine starting…” when a query begins, then “Engine ready” on success).

5. **Connection Pooling (Optional):**  
   - A simple connection pool reuses Firebolt connections between requests, improving performance.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/firebolt-demo.git
   cd firebolt-demo
   ```

2. **Create and Activate a Virtual Environment (Python 3.9 or Higher):**

   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**  
   Either create a `.env` file in the project root with your Firebolt credentials:

   ```ini
   FIREBOLT_CLIENT_ID=your_client_id
   FIREBOLT_CLIENT_SECRET=your_client_secret
   FIREBOLT_ENGINE_NAME=your_engine_name
   FIREBOLT_DATABASE=your_database
   FIREBOLT_ACCOUNT=your_account_name
   ```

   or set these variables in your hosting platform’s configuration.

5. **Set Up Your Mapbox Token:**  
   Create a file named `mapbox_token.txt` in the project root and paste your Mapbox public token (starting with "pk.") into it. Ensure there are no extra spaces or newlines.

## Running Locally

1. **Activate Your Virtual Environment:**

   ```bash
   source venv/bin/activate
   ```

2. **Run the Flask App:**

   ```bash
   python app.py
   ```

3. **Open Your Browser:**  
   Navigate to `http://localhost:5000`.

This demo highlights how Firebolt can rapidly process geospatial queries and return data for real-time map visualization. Use the search and filter options to see:

- Rapid querying based on spatial data.
- Dynamic map updates in clustered and heatmap views.
- Real-time query metrics and engine status messages to demonstrate performance.
