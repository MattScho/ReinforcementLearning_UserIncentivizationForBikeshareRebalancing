import json
import time
EXPORTFILE = "NYC.json"



first_lr = 0

with open(EXPORTFILE, 'r') as data:
    data = data.read()
    '''
    data = data.replace("si", "station_id")
    data = data.replace("bi", "bcycle_indego")
    data = data.replace("nba", "num_bikes_available")
    data = data.replace("nda", "num_docks_available")
    data = data.replace("inst", "is_installed")
    data = data.replace("rntng", "is_renting")
    data = data.replace("rtrng", "is_returning")
    data = data.replace("lr", "last_reported")
    '''
    data = data.split("\n")[:-1]
    lengthOfDate = len(data)
    dataLenPercentage = int(lengthOfDate * .01)
    unit = data[-2]
    unit = json.loads(unit)
    last_lr = unit["last_updated"]
    unit = data[0]
    unit = json.loads(unit)
    first_lr = unit["last_updated"]
    for i in range(100):
        start = time.time()
        writeOut = ""
        print(i)
        dataX = data[dataLenPercentage * i : dataLenPercentage * (i+1)]
        for unit in dataX:
            unit = json.loads(unit)
            for station in unit["data"]["stations"]:
                writeOut += str(station["lr"]) + "," + str(station["si"]) + "," + \
                    str(station["nba"]) + "," + str(station["nda"]) + "," + \
                    str(station["inst"]) + ","  + str(station["rntng"]) + "," + str(station["rtrng"]) + "\n"


        with open("NYC_data_" + str(first_lr) + "_to_" + str(last_lr) + ".csv", "a+") as file:
            file.write(writeOut)
            file.close()
        print(time.time() - start)