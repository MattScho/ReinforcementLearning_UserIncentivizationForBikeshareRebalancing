import json
EXPORTFILE = "ATL.json"


writeOut = ""

first_lr = 0

with open(EXPORTFILE, 'r') as data:
    data = data.read()
    data = data.replace("si","station_id")
    data = data.replace("nba", "num_bikes_available")
    data = data.replace("nda", "num_docks_available")
    data = data.replace("inst", "is_installed")
    data = data.replace("rntng", "is_renting")
    data = data.replace("rtrng", "is_returning")
    data = data.replace("lr", "last_reported")
    data = data.replace("h", "hub_")
    data = data.replace("nbd", "num_bikes_disabled")
    data = data.split("\n")
    first = True
    for unit in data[:-1]:
        unit = json.loads(unit)
        if first:
          first = False
          first_lr = unit["last_updated"]
        for station in unit["data"]["stations"]:
            print(station["last_reported"])
            writeOut += str(station["last_reported"]) + "," + str(station["station_id"]) + "," + \
                str(station["num_bikes_available"]) + ","  + \
                str(station["num_bikes_disabled"]) + "," + str(station["num_docks_available"]) + "," + str(station["is_installed"]) + ","+ str(station["is_renting"]) + "," + str(station["is_returning"]) + '\n'
                
    unit = data[-2]
    unit = json.loads(unit)
    last_lr = unit["last_updated"]

with open("ATL_data_" + str(first_lr) + "_to_" + str(last_lr) + ".csv", "w+") as file:
    file.write(writeOut)
    file.close()
