import pandas as pd
import matplotlib.pyplot as plt

budget = 10000
target = "_10000_4500"
name_pattern = "*gamesBudget" + str(budget) + target + ".csv"

files = []
labels = ["SADUE-A", "S-A", "S-A+", "SA'D'-A+", "SA'D'-A+D+"]
for v in range(1,6):
    files.append("../global/DC_base/v"+str(v)+"_gamesBudget" + str(budget) + target + ".csv")

for j, file in enumerate(files):
    frame = pd.read_csv(file, names=["Number_of_Users", "Serviced_Users", "Unserviced_Users",
                                                 "Potential_Unserviced_Users", "Resolved_Users", "Budget"], skiprows=3)
    frame["Service_Level"] = frame["Serviced_Users"]/frame["Number_of_Users"]

    vals = []
    for i in range(int(len(frame["Service_Level"])/100)):
        vals.append(sum(frame["Service_Level"][i*100:(i+1)*100])/100)

    plt.scatter(range(len(vals)), vals, label=labels[j])
target = target.replace("_", " ")
plt.legend(loc="upper left", fontsize=24)
plt.ylabel("Service Level")
plt.xlabel("Number of Games (100 games)")
plt.show()