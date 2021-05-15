import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np

'''
Settings
'''
end_perfs = {}

# Directory containing results
results_directory = "../global/DC_base/"

# Metric improvement to visualize
metric = "Service_Level"

budgets = [300, 1000, 2000, 4000, 10000]

# Step through budgets
for supply in [450, 2250, 3375, 4500]:
    for users in [5000, 10000, 15000]:
        # Budget file name pattern
        target = "_"+str(users)+"_"+str(supply)

        # Initialize data and error recorders
        data = {
            "v1": [],
            "v2": [],
            "v3": [],
            "v4": [],
            "v5": []
        }

        # Set budgets
        budgets = [300, 1000, 2000, 4000, 10000]

        # Step through budgets
        for budget in budgets:
            name_pattern = "*gamesBudget" + str(budget) + target + ".csv"

            # Learning rate files
            step_files = glob.glob(results_directory + name_pattern)
            print(len(step_files))

            # Calculate no agent
            no_op_frame = pd.read_csv(results_directory + "\\noAgent_games"+target +".csv", names=["Number_of_Users", "Serviced_Users", "Unserviced_Users",
                                                     "Potential_Unserviced_Users", "Resolved_Users", "Budget"], skiprows=3)

            no_op_frame["Service_Level"] = no_op_frame["Serviced_Users"] / no_op_frame["Number_of_Users"]
            no_op_value = sum(no_op_frame[metric].values)/len(no_op_frame[metric].values)

            # Step through retrieved files
            for i, file in enumerate(step_files):

                # Read in file
                frame = pd.read_csv(file, names=["Number_of_Users", "Serviced_Users", "Unserviced_Users",
                                                     "Potential_Unserviced_Users", "Resolved_Users", "Budget"], skiprows=3)

                frame["Service_Level"] = frame["Serviced_Users"] / frame["Number_of_Users"]

                # Get results, using the last 100 indices of the steps
                results = frame[metric].values[-100:]

                # Grab version to make title
                v = file.split("_games")[-2].split("\\")[-1]

                print(sum(results) / len(results))
                print(no_op_value)
                print()
                # Store metric calculations
                data[v].append(sum(results) / len(results))

        end_perfs[target] = data

# Sum budgets
for k in end_perfs.keys():
    for k_r in end_perfs[k].keys():
        end_perfs[k][k_r] = sum(end_perfs[k][k_r])/len(budgets)
    accumulation = 0
    for reps in range(1,6):
        accumulation += end_perfs[k]["v"+str(reps)]
        # Average across 5 representations
    end_perfs[k] = accumulation / 5

# Reformat into a matrix for a heatmap
output = []
for k in end_perfs.keys():
    output.append(end_perfs[k])
np_output = np.array(output).reshape((4,3,))

# Create heatmap
heatmap = plt.pcolor(np_output, cmap="Greens")
plt.xlim([0,3])
plt.ylim([0,4])
plt.xticks([i+0.5 for i in  range(3)], ["5000", "10000", "15000"], fontsize=24)
plt.yticks([i+0.5 for i in range(4)], ["450", "2250", "3375", "4500"], fontsize=24)
cbar = plt.colorbar(heatmap, cmap="Greens")
cbar.ax.tick_params(labelsize=32)
plt.xlabel("Users", fontsize=32)
plt.ylabel("Supply", fontsize=32)
plt.title("Service Level", fontsize=32)
plt.show()