'''
Load Trip data between 2010 - 2019

:author: Matthew Schofield
:version: 5.15.2021
'''
from bikeshare_db.trip import Trip
import time
from bikeshare_db import session
import glob
import json

# Log start time for information while script runs
init_start = time.time()

# Map stations to (lat,lon)
station_lat_lon = {}
# Read in station information JSON
try:
    station_info = json.loads(open("../raw_data/station_info.json", 'r').read())
except:
    print("ERROR: Could not find raw data directory, not included in GitHub repository contact Matthew Schofield"
          " for raw data or use your own")
    exit(1)

# Create hash table to map station names to lat,lon
for station in station_info["data"]["stations"]:
    station_lat_lon[station["short_name"]] = [station["lat"], station["lon"]]

# Boundaries for region, with adjustments to shrink system size
upper_lat = 38.935
lower_lat = 38.86 + 0.015
upper_lon = -76.98
lower_lon = -77.14 + 0.04
lat_range = upper_lat - lower_lat
lon_range = upper_lon - lower_lon

# Read in files
for file in glob.glob("../raw_data/trip_data/201[5-9]*.csv"):
    # File start time
    start = time.time()
    print(file)
    # Get lines of the file, each trip record
    lines = open(file, 'r').read().replace("\"", "").split("\n")[1:-1]
    # Step through lines
    for line in lines:
        # Grab elements of trip data
        line = line.split(",")
        duration = int(line[0])
        start_date = line[1]
        end_date = line[2]
        start_station_number = line[3]
        end_station_number = line[5]
        bike_number = line[7]
        member_type = line[8]

        # Calculate day epoch values
        split_start_date = start_date.split(":")
        day_epoch_start = (int(split_start_date[0][-2:]) * 3600) + (int(split_start_date[1]) * 60) + int(split_start_date[2])
        split_end_date = end_date.split(":")
        day_epoch_end = (int(split_end_date[0][-2:]) * 3600) + (int(split_end_date[1]) * 60) + int(split_end_date[2])

        # Get Lat,Lon
        start_station_lat = station_lat_lon.get(start_station_number, [-1, -1])[0]
        start_station_lon = station_lat_lon.get(start_station_number,[-1, -1])[1]

        end_station_lat = station_lat_lon.get(end_station_number, [-1, -1])[0]
        end_station_lon = station_lat_lon.get(end_station_number, [-1, -1])[1]

        # Calculate location region
        start_r_x = int(((start_station_lon - lower_lon)/lon_range)*10)
        start_r_y = int(((start_station_lat - lower_lat)/lat_range)*10)
        end_r_x = int(((end_station_lon - lower_lon)/lon_range)*10)
        end_r_y = int(((end_station_lat - lower_lat)/lat_range)*10)

        # Only accepts locations that are in the 10x10 system, i.e. regions [0,9]
        if start_r_x  >= 0 and start_r_x <= 9 and \
            start_r_y >= 0 and start_r_y <= 9 and \
            end_r_x >= 0 and end_r_x <= 9 and \
            end_r_y >= 0 and end_r_y <= 9:
            # Create Trip record
            Trip.create_trip(duration, start_date, end_date, start_station_number, end_station_number, bike_number,
                             member_type, day_epoch_start, day_epoch_end, start_station_lat, start_station_lon,
                            end_station_lat, end_station_lon, start_r_x, start_r_y, end_r_x, end_r_y)
    # Commit set of trip records
    session.commit()
    # How long file took to process
    print("\t",time.time() - start)

# Show duration of trip
print("TOTAL TIME")
print(time.time() - init_start)