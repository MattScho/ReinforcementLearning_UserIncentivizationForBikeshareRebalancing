import pandas as pd
import matplotlib.pyplot as plt
import glob as glob
from statistics import mean

'''
View a comparison of learning rate

:author: Matthew Schofield
:version: 2.3.2021
'''
'''
Settings
'''

# Set metric
metric = "Service Level"

# Result directories
pattern = {
    "PPO": "../global/DC_base_algs/PPO*Budget4000*",
    "ACKTR": "../global/DC_base_algs/ACKTR*Budget4000*"
}

# Algorithms compared
rl_algorithms = ["PPO",  "ACKTR"]

'''
Execution
'''
# Learning time series storage
learning_time_series = {}

for rl in rl_algorithms:
    learning_time_series[rl] = []

# Step through results
for alg in rl_algorithms:
    # Learning rate files
    step_files = glob.glob(pattern[alg])

    # Show step files accumulated
    print("Number of files: " + str(len(step_files)))
    print(step_files)

    # Step through retrieved files
    for i, file in enumerate(step_files):
        frame = pd.read_csv(file, names=["Number_of_Users", "Serviced_Users", "Unserviced_Users",
                                                     "Potential_Unserviced_Users", "Resolved_Users", "Budget"], skiprows=3)
        frame["Service_Level"] = frame["Serviced_Users"]/frame["Number_of_Users"]

        vals = []
        for i in range(int(len(frame["Service_Level"])/100)):
            vals.append(sum(frame["Service_Level"][i*100:(i+1)*100])/100)
        learning_time_series[alg].append(vals)

linestyles = ["-.", "--", ":"]
markers = ["s",  "o"]
colors = ["#1f77b4", "g"]

average_of_learning = {}

for alg in learning_time_series.keys():
    average_of_learning[alg] = list(map(mean, zip(*learning_time_series[alg])))

# Plot results
for l, alg in enumerate(average_of_learning.keys()):
    plt.plot(range(len(average_of_learning[alg])), average_of_learning[alg], label=alg, linestyle=linestyles[l], marker=markers[l], color=colors[l], linewidth=5, markersize=18)
plt.xlabel("Episodes (100)", fontsize=32)
plt.yticks([0.86, 0.88, 0.9, 0.92, 0.94], labels=[0.86, 0.88, 0.9, 0.92, 0.94], fontsize=32)
plt.xticks([0, 20, 40, 60, 80, 100], [0, 20, 40, 60, 80, 100], fontsize=32)
plt.ylabel("Service Level", fontsize=32)
plt.legend(loc="upper left", fontsize=32)
plt.show()
