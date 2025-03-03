// Set up Mapbox token from the global variable injected by index.html
mapboxgl.accessToken = window.MAPBOX_TOKEN;

// Global variables
let lastGeoJSON = null;
let currentView = 'cluster'; // "cluster" or "heatmap"
let currentLocation = "Santa Monica, California, United States"; // initial default

// Update engine status in Query Info panel
function setEngineStatus(msg) {
  const engStatusEl = document.getElementById('engine-status');
  if (engStatusEl) engStatusEl.textContent = msg;
}

// Initialize the map
function initializeMap(centerCoords) {
  const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: centerCoords,
    zoom: 12,
    scrollZoom: { speed: 0.05, easing: t => t }
  });

  map.addControl(new mapboxgl.NavigationControl(), 'bottom-right');

  const geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    marker: false,
    placeholder: 'Search location...',
    zoom: 12
  });
  map.addControl(geocoder, 'top-right');

  geocoder.on('result', (e) => {
    currentLocation = e.result.place_name;
    map.flyTo({ center: e.result.center, zoom: 12 });
    loadAccidents(currentLocation, map);
  });

  map.on('load', () => {
    loadAccidents(currentLocation, map);
  });

  setUpControls(map);

  function attachPopup(layerName) {
    map.on('click', layerName, (e) => {
      const features = map.queryRenderedFeatures(e.point, { layers: [layerName] });
      if (!features.length) return;
      const feature = features[0];
      const description = `
        <strong>Accident ID:</strong> ${feature.properties.id || 'N/A'}<br>
        <strong>Severity:</strong> ${feature.properties.severity || 'N/A'}<br>
        <strong>Time:</strong> ${feature.properties.start_time || 'N/A'}<br>
        <strong>Weather:</strong> ${feature.properties.weather_condition || 'N/A'}<br>
        <strong>Distance (mi):</strong> ${feature.properties.distance_mi || 'N/A'}<br>
        <strong>Description:</strong> ${feature.properties.description || 'N/A'}
      `;
      new mapboxgl.Popup()
        .setLngLat(feature.geometry.coordinates)
        .setHTML(description)
        .addTo(map);
    });
    map.on('mouseenter', layerName, () => { map.getCanvas().style.cursor = 'pointer'; });
    map.on('mouseleave', layerName, () => { map.getCanvas().style.cursor = ''; });
  }
  attachPopup('accidents-unclustered-point');
  attachPopup('accidents-circle');

  animateHeatmap(map);
}

// Load accident data
function loadAccidents(locationString, map) {
  // Update engine status to show startup message
  setEngineStatus('Engine starting...');
  
  let queryURL = '/geojson?location=' + encodeURIComponent(locationString);
  const severity = document.getElementById('severity-filter').value;
  const startYear = document.getElementById('start-year-range').value;
  const endYear = document.getElementById('end-year-range').value;

  if (severity) queryURL += '&severity=' + encodeURIComponent(severity);
  if (startYear) queryURL += '&start_date=' + encodeURIComponent(startYear + '-01-01');
  if (endYear) queryURL += '&end_date=' + encodeURIComponent(endYear + '-12-31');

  console.log(queryURL);
  const qi = document.getElementById('query-info');
  qi.style.display = document.getElementById('toggle-query-info').checked ? 'block' : 'none';

  fetch(queryURL)
    .then(resp => resp.json())
    .then(data => {
      // Update engine status to ready after data is fetched
      setEngineStatus('Engine ready');
      
      if (data.error) {
        removeAccidentLayers(map);
        lastGeoJSON = null;
        document.getElementById('accident-count').textContent = 'Accidents found: 0';
        return;
      }
      let geojson = data.geojson ? data.geojson : (data.features ? data : null);
      if (!geojson || !geojson.features || geojson.features.length === 0) {
        setEngineStatus('No results found');
        removeAccidentLayers(map);
        lastGeoJSON = null;
        document.getElementById('accident-count').textContent = 'Accidents found: 0';
        return;
      }
      lastGeoJSON = geojson;
      document.getElementById('query-time').textContent = 'Query time: ' + (data.query_time || '--') + ' s';
      document.getElementById('data-scanned').textContent = 'Data scanned: ' + (data.data_scanned || 'N/A');
      document.getElementById('accident-count').textContent = 'Accidents found: ' + (data.accident_count || geojson.features.length);
      setAccidentSource(currentView, map);
    })
    .catch(err => {
      console.error('Error loading /geojson data:', err);
      document.getElementById('query-string').textContent = 'Error loading data.';
      setEngineStatus('Engine error!');
    });
}

function removeAccidentLayers(map) {
  const layers = ['accidents-cluster', 'accidents-cluster-count', 'accidents-unclustered-point', 'accidents-heat', 'accidents-circle'];
  layers.forEach(layer => { if (map.getLayer(layer)) { map.removeLayer(layer); } });
  if (map.getSource('accidents')) { map.removeSource('accidents'); }
}

function setAccidentSource(viewType, map) {
  removeAccidentLayers(map);
  const useClustering = viewType === 'cluster';
  map.addSource('accidents', {
    type: 'geojson',
    data: lastGeoJSON,
    cluster: useClustering,
    clusterMaxZoom: 14,
    clusterRadius: 50
  });
  if (viewType === 'cluster') {
    addClusterLayers(map);
  } else if (viewType === 'heatmap') {
    addHeatmapLayer(map);
    map.addLayer({
      id: 'accidents-circle',
      type: 'circle',
      source: 'accidents',
      minzoom: 16,
      paint: {
        'circle-color': [
          'match',
          ['to-string', ['get', 'severity']],
          '1', '#00FF00',
          '2', '#FFFF00',
          '3', '#FFA500',
          '4', '#FF0000',
          '#999999'
        ],
        'circle-radius': 5,
        'circle-stroke-width': 1,
        'circle-stroke-color': '#000'
      }
    });
  }
}

function addClusterLayers(map) {
  map.addLayer({
    id: 'accidents-cluster',
    type: 'circle',
    source: 'accidents',
    filter: ['has', 'point_count'],
    paint: {
      'circle-color': [
        'step',
        ['get', 'point_count'],
        '#51bbd6',
        100,
        '#f1f075',
        750,
        '#f28cb1'
      ],
      'circle-radius': [
        'step',
        ['get', 'point_count'],
        20,
        100,
        30,
        750,
        40
      ]
    }
  });
  map.addLayer({
    id: 'accidents-cluster-count',
    type: 'symbol',
    source: 'accidents',
    filter: ['has', 'point_count'],
    layout: {
      'text-field': '{point_count_abbreviated}',
      'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
      'text-size': 12
    }
  });
  map.addLayer({
    id: 'accidents-unclustered-point',
    type: 'circle',
    source: 'accidents',
    filter: ['!', ['has', 'point_count']],
    paint: {
      'circle-color': [
        'match',
        ['to-string', ['get', 'severity']],
        '1', '#00FF00',
        '2', '#FFFF00',
        '3', '#FFA500',
        '4', '#FF0000',
        '#999999'
      ],
      'circle-radius': 5,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#000'
    }
  });
}

function addHeatmapLayer(map) {
  map.addLayer({
    id: 'accidents-heat',
    type: 'heatmap',
    source: 'accidents',
    paint: {
      'heatmap-weight': [
        'interpolate',
        ['linear'],
        ['to-number', ['get', 'severity']],
        1, 0.25,
        4, 1.0
      ],
      'heatmap-intensity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0, 0.5,
        9, 1.0,
        15, 2.0
      ],
      'heatmap-color': [
        'interpolate',
        ['linear'],
        ['heatmap-density'],
        0, 'rgba(144,238,144,0)',
        0.2, 'rgb(144,238,144)',
        0.4, 'rgb(255,255,0)',
        0.6, 'rgb(255,165,0)',
        1, 'rgb(178,24,43)'
      ],
      'heatmap-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0, 2,
        9, 15,
        15, 35
      ],
      'heatmap-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        7, 0.7,
        15, 0.9
      ]
    }
  });
}

function animateHeatmap(map) {
  if (currentView === 'heatmap' && map.getLayer('accidents-heat')) {
    const zoom = map.getZoom();
    let baseIntensity = zoom <= 7 ? 1 : (zoom >= 15 ? 5 : 1 + ((zoom - 7) * (4 / 8)));
    const pulse = 1 + 0.2 * Math.sin(performance.now() / 300);
    const newIntensity = baseIntensity * pulse;
    map.setPaintProperty('accidents-heat', 'heatmap-intensity', newIntensity);
  }
  requestAnimationFrame(() => animateHeatmap(map));
}

function setUpControls(map) {
  document.getElementsByName('viz').forEach(radio => {
    radio.addEventListener('change', e => {
      currentView = e.target.value;
      if (lastGeoJSON) setAccidentSource(currentView, map);
    });
  });

  document.getElementById('toggle-query-info').addEventListener('change', e => {
    const qi = document.getElementById('query-info');
    qi.style.display = e.target.checked ? 'block' : 'none';
  });

  const severitySelect = document.getElementById('severity-filter');
  severitySelect.addEventListener('change', () => {
    loadAccidents(currentLocation, map);
  });

  const startYearSlider = document.getElementById('start-year-range');
  const startYearVal = document.getElementById('start-year-val');
  startYearSlider.addEventListener('input', () => {
    startYearVal.textContent = startYearSlider.value;
    loadAccidents(currentLocation, map);
  });

  const endYearSlider = document.getElementById('end-year-range');
  const endYearVal = document.getElementById('end-year-val');
  endYearSlider.addEventListener('input', () => {
    endYearVal.textContent = endYearSlider.value;
    loadAccidents(currentLocation, map);
  });

  const styleSwitcher = document.getElementById('style-switcher');
  styleSwitcher.addEventListener('click', e => {
    if (e.target.tagName.toLowerCase() === 'button') {
      const newStyle = e.target.getAttribute('data-style');
      map.setStyle(newStyle);
      map.once('idle', () => {
        if (lastGeoJSON) setAccidentSource(currentView, map);
      });
    }
  });
}

// Reverse geocode the default location using currentLocation and initialize map.
const defaultURL = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(currentLocation)}.json?access_token=${mapboxgl.accessToken}`;
fetch(defaultURL)
  .then(resp => resp.json())
  .then(data => {
    let centerCoords = [-118.55, 33.98]; // fallback (Santa Monica)
    if (data.features && data.features.length > 0) {
      centerCoords = data.features[0].center;
    }
    initializeMap(centerCoords);
  })
  .catch(err => {
    console.error("Error fetching default location:", err);
    initializeMap([-119.55, 39.98]);
  });
