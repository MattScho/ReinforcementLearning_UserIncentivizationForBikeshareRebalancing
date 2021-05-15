import pandas as pd
import matplotlib.pyplot as plt
import glob

'''
Process
'''

'''
Settings
'''
supplies = ["4500", "3375", "2250"]


# Initialize data and error recorders
data = {
    "4500": [0, 0, 0, 0, 0],
    "3375": [0, 0, 0, 0, 0],
    "2250": [0, 0, 0, 0, 0]
}

no_opt = {
    "p": [0,0,0],
    "o": [0,0,0]
}


'''
Settings
'''
for supply in [4500, 3375, 2250]:
    for users in [5000, 10000, 15000]:
        # Budget file name pattern
        target = "_"+str(users)+"_"+str(supply)
        # Directory containing results
        results_directory = "../global/DC_base"

        # Metric improvement to visualize and y limit range
        # Either ["Reduced Unservice", "Service Level", "Budget"]
        metric = "Service Level"

        # Vary this to focus on a particular y range, though pyplot's zoom feature could be used
        # If interested in viewing the Budget metric comment out line "plt.setp(axs, ylim=ylimits)"
        ylimits = [0.65, 1.0]

        # Set budgets
        budgets = [300, 1000, 2000, 4000, 10000]

        for budget in budgets:
            # Budget file name pattern
            name_pattern = "*gamesBudget" + str(budget) + target + ".csv"

            # Learning rate files
            step_files = glob.glob(results_directory + "\\" + name_pattern)

            step_files.append(results_directory + "\\noAgent_games" + target + ".csv")
            step_files.append(results_directory + "\\opt_games" + target + ".csv")
            # Step through retrieved files
            for i, file in enumerate(step_files):
                # Read in file
                frame = pd.read_csv(file, names=["Number_of_Users", "Serviced_Users", "Unserviced_Users",
                                                 "Potential_Unserviced_Users", "Resolved_Users", "Budget"],
                                    skiprows=3)
                frame["Service Level"] = frame["Serviced_Users"] / frame["Number_of_Users"]

                # Get results, using the last 100 indices of the steps
                results = frame[metric].values[-100:]

                # Grab version to make title
                v = file.split("_games")[-2].split("\\")[-1][1]

                if v in ["p", "o"]:
                    no_opt[v][supplies.index(str(supply))] += (sum(results) / len(results))/15
                else:
                    data[str(supply)][int(v)-1] += (sum(results) / len(results))/15

plt.ylim([0.65, 1.0])
data_out = []

for i in range(5):
    data_out.append([])
    for k in data.keys():
        data_out[i].append(data[k][i])


markers = ["s", "^", "o", "p", "+", "x"]

print(no_opt)
no_opt_data = []
for k in no_opt.keys():
    no_opt_data.append(no_opt[k])

no_opt_labels = ["No Agent", "Emp. Optimal"]
for l, data in enumerate(no_opt_data):
    plt.plot(supplies, data, linestyle="--", linewidth=5, label=no_opt_labels[l], markersize=24)

print(data_out)
for l, data in enumerate(data_out):
    plt.plot(supplies, data, linestyle="--", marker=markers[l], linewidth=5, label=budgets[l], markersize=24)

plt.legend(loc="upper right", fontsize=20)

plt.ylabel("Service Level", fontsize=32)
plt.xlabel("Supply", fontsize=32)

# Style plot axis X ticks
plt.xticks(range(len(supplies)), labels=["4500", "3375 (-25%)", "2250 (-50%)"], fontsize=24)
plt.yticks([0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0], labels=[0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0], fontsize=24)
plt.show()
