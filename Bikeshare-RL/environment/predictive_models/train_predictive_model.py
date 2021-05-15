import pickle as pkl
import numpy as np
from keras.layers import Dense, LSTM
from keras.models import Sequential

'''
Train a predictive model for predicting departures per region based on previous timesteps

:author: Matthew Schofield
:version: 4.10.2021
'''

# Set-up inits
OUTPUT_DIR = "model/"
ENV_INIT = "../generated_environments/DC_base.pkl"

# Load in environment
env_init_file = pkl.load(open(ENV_INIT, "rb"))
users_per_hour = env_init_file.get_user_per_hour()
arrival_distribs = env_init_file.get_arrivals()

# Set some env parameters, try to have the users parameter close to the range that will be used in practice as to best
# capture noise in the distribution
# Days determines the number of generated distributions for training
users = 10000
days = 100

# Empty list to store generated matrices
arrival_matrices = []
# Indexes regions [1, 2, 3, ..., 99, 100]
region_indices = np.arange(100)

# Set-up data
# Builds a list of in order arrival matrices, size is days * 24 hours
for i in range(days):
    # Step through 24h
    for hour in range(24):
        # Zeroes 100 len vector that will be added to and reshaped into a 10x10 matrix
        arrivals = np.zeros(100, )
        # Users for the hour
        users_in_sample = int(users * users_per_hour[hour])
        # For each user assign them to an arrival region based on the hourly arrival distribution
        for u in range(users_in_sample):
            arrivals[np.random.choice(region_indices, p=arrival_distribs[hour])] += 1
        # Normalize such that the sum of all elements == 1
        arrivals = np.divide(arrivals, np.sum(arrivals))
        # Add matrix to list of ordered arrival matrices for later training
        arrival_matrices.append(arrivals)

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=3):
    # Feature matrices will go in X and target matrices go in Y
    # Features       Predicts
    # D_-3 D_-2 D_-1 => D_0
    # For Example
    # D_14 D_15 D_16 => D_17
    # Then
    # D_15 D_16 D_17 => D_18
    # and so on until the last D_n is reached
    dataX, dataY = [], []
    # Step through the given dataset and create a lookback training set detailed above
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return np.array(dataX), np.array(dataY)

# Use the above function to craft dataset
X, y = create_dataset(arrival_matrices)
# Classic 80-20 Train Test split
train_x = X[:int(len(X)*.8)]
test_x = X[int(len(X)*.8):]
train_y = y[:int(len(y)*.8)]
test_y = y[int(len(y)*.8):]

# Set-up model
# Feed forward
model = Sequential()
# Core of the model 10 LSTM nodes
model.add(LSTM(10, activation='relu', input_shape=(3, 100)))
# Clean up layers
model.add(Dense(100))
model.add(Dense(100))
# Compile to prep model for training
model.compile(optimizer='adam', loss='mse')

# Fit model
model.fit(train_x, train_y, epochs=1000)

# Save model
model.save(OUTPUT_DIR + "arrival_pred.mdl")
