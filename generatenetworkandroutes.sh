#!/bin/bash

# Check arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <osm-map.osm> <counts.xml> <fringe-factor>"
    exit 1
fi

# Input arguments
OSM_FILE="$1"
COUNTS_FILE="$2"
FRINGE_FACTOR="$3"

# Intermediate/output files
NETWORK_FILE="network.net.xml"
TRIPS_FILE="trips.xml"
INITIAL_ROUTES="routes_initial.rou.xml"
FINAL_ROUTES="routes.rou.xml"

# Step 1: Convert OSM map to SUMO network
netconvert --osm-files "$OSM_FILE" --no-turnarounds -o "$NETWORK_FILE"

# Step 2: Generate random trips
python3 "C:/ProgramFiles/Sumo/tools/randomTrips.py" \
    -n "$NETWORK_FILE" \
    --fringe-factor "$FRINGE_FACTOR" \
    -o "$TRIPS_FILE"

# Step 3: Generate initial routes
duarouter \
    -n "$NETWORK_FILE" \
    -t "$TRIPS_FILE" \
    -o "$INITIAL_ROUTES"

# Step 4: Sample routes using edge counts
python3 "C:/ProgramFiles/Sumo/tools/routeSampler.py" \
    -r "$INITIAL_ROUTES" \
    --edgedata-files "$COUNTS_FILE" \
    -o "$FINAL_ROUTES"

echo "Pipeline completed successfully."