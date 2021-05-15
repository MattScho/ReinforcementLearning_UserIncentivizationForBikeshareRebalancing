'''
Build interest distributions

arrival interests - Distribution of user arrival interests per hour
destination interests - Distribution of user destination interests per hour
users per hour - Relative number of users per hour
supply - layout of bicycles across regions

:author: Matthew Schofield
'''
import numpy as np
import pickle as pkl

# Spatio-Temporal environment settings
regions = 10**2
timeslots = 24

# Init distributions
arrival_interests = np.zeros((24,100))
destination_interests = np.zeros((24,100,100))
hour_counts = np.zeros((24,))
supply = np.zeros((100,))

'''
Trip data 2010 - 2019
'''
import time
import glob
import json

# Start time for information
init_start = time.time()

station_lat_lon = {}
station_info = json.loads(open("../raw_data/station_info.json", 'r').read())
# Create hash table to map station names to lat,lon
for station in station_info["data"]["stations"]:
    station_lat_lon[station["short_name"]] = [station["lat"], station["lon"]]

# Boundaries for region
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

        # Calculate region
        start_r_x = int(((start_station_lon - lower_lon)/lon_range)*10)
        start_r_y = int(((start_station_lat - lower_lat)/lat_range)*10)
        end_r_x = int(((end_station_lon - lower_lon)/lon_range)*10)
        end_r_y = int(((end_station_lat - lower_lat)/lat_range)*10)

        # Check within region bounds
        if start_r_x  >= 0 and start_r_x <= 9 and \
            start_r_y >= 0 and start_r_y <= 9 and \
            end_r_x >= 0 and end_r_x <= 9 and \
            end_r_y >= 0 and end_r_y <= 9:
            a = start_r_x + start_r_y*10
            d = end_r_x + end_r_y * 10
            h = int(day_epoch_start / 3600)
            # Supply based on 6pm supply distribution
            if h == 17:
                supply[d] += 1
            hour_counts[h] += 1
            # Add to user arrival and destination interests
            arrival_interests[h][a] += 1
            for w in range(100):
                destination_interests[h][w][d] += 1

    # How long file took
    print("\t",time.time() - start)
print("TOTAL TIME")
print(time.time() - init_start)

# Normalize arrival and destination interest distributions
for hour in range(24):
    users = hour_counts[hour]
    print(users)
    arrival_interests[hour] = np.divide(arrival_interests[hour], np.sum(arrival_interests[hour]))
    for a in range(100):
        if np.sum(destination_interests[hour][a]) == 0:
            destination_interests[hour][a] = np.divide(np.ones(100,), np.sum(np.ones((100,))))
        else:
            destination_interests[hour][a] = np.divide(destination_interests[hour][a], np.sum(destination_interests[hour][a]))

# Normalize hourly and supply distributions
hour_counts = np.divide(hour_counts, np.sum(hour_counts))
supply = np.divide(supply, np.sum(supply))

# Save outputs to files
pkl.dump(hour_counts, open("distributions/hourly_user.pkl", "wb+"))
pkl.dump(supply, open("distributions/supply.pkl", "wb+"))
pkl.dump(arrival_interests, open("distributions/arrival.pkl", "wb+"))
pkl.dump(destination_interests, open("distributions/destination.pkl", "wb+"))
