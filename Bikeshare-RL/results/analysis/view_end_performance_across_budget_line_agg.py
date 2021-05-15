import pandas as pd
import matplotlib.pyplot as plt
import glob
from statistics import stdev

'''
Process
'''
# Initialize data and error recorders
data = {
    "opt": [0, 0, 0, 0, 0],
    "noAgent": [0, 0, 0, 0, 0],
    "v1": [0, 0, 0, 0, 0],
    "v2": [0, 0, 0, 0, 0],
    "v3": [0, 0, 0, 0, 0],
    "v4": [0, 0, 0, 0, 0],
    "v5": [0, 0, 0, 0, 0]
}

counts = {
    "opt": 0,
    "noAgent": 0,
    "v1": 0,
    "v2": 0,
    "v3": 0,
    "v4": 0,
    "v5": 0
}


'''
Settings
'''
# Step through budgets
for supply in [4500, 3375, 2250, 450]:
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
        ylimits = [0.65, 0.9]

        # Set budgets
        budgets = [300, 1000, 2000, 4000, 10000]

        # Step through budgets
        for budget in budgets:
            # Budget file name pattern
            name_pattern = "*gamesBudget" + str(budget) + target + ".csv"

            # Learning rate files
            step_files = glob.glob(results_directory + "\\" + name_pattern)

            # Add no agent and opt files
            step_files.append(results_directory + "\\opt_games" + target + ".csv")
            step_files.append(results_directory + "\\noAgent_games" + target + ".csv")


            # Step through retrieved files
            for i, file in enumerate(step_files):
                print(file)
                # Read in file
                frame = pd.read_csv(file, names=["Number_of_Users", "Serviced_Users", "Unserviced_Users",
                                                 "Potential_Unserviced_Users", "Resolved_Users", "Budget"], skiprows=3)
                frame["Service Level"] = frame["Serviced_Users"]/frame["Number_of_Users"]

                # Get results, using the last 100 indices of the steps
                results = frame[metric].values[-100:]

                # Grab version to make title
                v = file.split("_games")[-2].split("\\")[-1]

                data[v][budgets.index(budget)] += (sum(results) / len(results))


# Average across settings
for k in data.keys():
    data[k] = [i/12 for i in data[k]]


# Construct plot
fig, ax = plt.subplots()

print(data)

legend_mapper = {
    "opt": "Epr. Optimal",
    "noAgent": "No Agent",
    "v1": "SADUE-A",
    "v2": "S-A",
    "v3": "S-A+",
    "v4": "SAD'-A+",
    "v5": "SA'D'-A+D+"
}

# Plot data
for k in data.keys():
    plt.plot(budgets, data[k], linestyle="--", linewidth=5, label=legend_mapper[k])
    plt.scatter(budgets, data[k], s=96)
    plt.xscale('log')
    plt.xticks(budgets, budgets, fontsize=24)
    plt.yticks([0.65, 0.7, 0.75, 0.8, 0.85, 0.9], fontsize=24)

#plt.legend(loc="upper left", fontsize=24)
# Set plot labels
plt.ylabel("Service Level", fontsize=32)
plt.xlabel("Budget ($ - USD)", fontsize=32)

plt.show()
