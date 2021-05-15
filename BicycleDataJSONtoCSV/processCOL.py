import json
#COL
EXPORTFILE = "COL.json"



first_lr = 0

with open(EXPORTFILE, 'r') as data:
    data = data.read()
    data = data.split("\n")
    out = ""
    first = True
    for unit in data[:-1]:
        unit = unit.replace("si", "station_id")
        unit = unit.replace("nba", "num_bikes_available")
        unit = unit.replace("nbd", "num_bikes_disabled")
        unit = unit.replace("nda", "num_docks_available")
        unit = unit.replace("ndd", "num_docks_disabled")
        unit = unit.replace("inst", "is_installed")
        unit = unit.replace("rntng", "is_renting")
        unit = unit.replace("rtrng","is_returning")
        unit = unit.replace("lr", "last_reported")
        unit = json.loads(unit)
        if first:
          first = False
          first_lr = unit["last_updated"]
        for station in unit["data"]["stations"]:
            date = station["last_reported"]
            print(date)
            out +=  str(station["last_reported"]) + "," + \
                str(station["station_id"]) + "," + str(station["num_bikes_available"]) + "," + \
                str(station["num_bikes_disabled"]) + "," + str(station['num_docks_available']) + "," + \
                str(station['num_docks_disabled']) + "," + str(station["is_installed"]) + "," + str(station["is_renting"]) + "," + str(station["is_returning"]) + '\n'
                
    unit = data[-2]
    unit = json.loads(unit)
    last_lr = unit["last_updated"]
with open("COL_data_" + str(first_lr) + "_to_" + str(last_lr) + ".csv", "w+") as file:
    file.write(out)
    file.close()