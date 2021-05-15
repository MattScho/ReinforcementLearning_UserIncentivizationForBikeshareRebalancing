import json
EXPORTFILE = "PHL.json"


writeOut = ""

first_lr = 0

with open(EXPORTFILE, 'r') as data:
    data = data.read()
    '''
    data = data.replace("si", "station_id")
    data = data.replace("bi", "bcycle_indego")
    data = data.replace("nba", "num_bikes_available")
    data = data.replace("nda", "num_docks_available")
    data = data.replace("inst" , "is_installed")
    data = data.replace("rntng", "is_renting")
    data = data.replace("rtrng", "is_returning")
    data = data.replace("lr", "last_reported")
    '''
    first = True
    data = data.split("\n")
    for unit in data[:-1]:
        unit = json.loads(unit)
        if first:
          first = False
          first_lr = unit["last_updated"]
        for station in unit["data"]["stations"]:
            writeOut += str(station["lr"]) + "," + str(station["si"]) + "," + \
                str(station["nba"]) + "," + str(station["nda"]) + "," + \
                str(station["inst"]) + ","  + str(station["rntng"]) + "," + str(station["rtrng"]) + "\n"
    unit = data[-2]
    unit = json.loads(unit)
    last_lr = unit["last_updated"]
with open("PHL_data_" + str(first_lr) + "_to_" + str(last_lr) + ".csv", "w+") as file:
    file.write(writeOut)
    file.close()
