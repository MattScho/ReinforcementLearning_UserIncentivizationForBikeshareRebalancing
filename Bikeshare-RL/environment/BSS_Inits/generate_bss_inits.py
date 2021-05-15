from environment.BSS_Inits.bss_env_init import BSS_Env_Init
import pickle as pkl
'''
Script to put together initialization distributions into a bss_env_init pkl file

SEE bss_env_init.py FOR INFORMATION ABOUT DISTRIBUTION .pkl FILE FORMATTING
'''
# paths
base_dir = "DC_base"
HOURLY_DISTRIB = open(base_dir + "/hourly_user.pkl", "rb")
DESTINATION_DISTRIB = open(base_dir + "/destination.pkl", "rb")
ARRIVAL_DISTRIB = open(base_dir + "/arrival.pkl", "rb")
SUPPLY_DISTRIB = open(base_dir + "/supply.pkl", "rb")

# Construct settings for bss init
title = "DC_Base"
description = "Initialization criteria based on DC's Capital Bikeshare 2015-2019 user trip activity data"
# Steps for simulation 24h = 24 timeslots
steps = 24

# 10x10 grid
system_length = 10

# Distribution for probability a user is at a particular hour
user_hourly_distrib = pkl.load(HOURLY_DISTRIB)
print("User Hourly Distribution Shape Check")
print(user_hourly_distrib.shape == (24,))

supply_distrib = pkl.load(SUPPLY_DISTRIB)
print("Supply Distribution Shape Check")
print(supply_distrib.shape == (system_length**2,))

arrival_distrib = pkl.load(ARRIVAL_DISTRIB)
print("User Arrival Distribution Shape Check")
print(arrival_distrib.shape == (24,system_length**2))

destinations_distrib = pkl.load(DESTINATION_DISTRIB)
print("User Destination Distribution Shape Check")
print(destinations_distrib.shape == (24,system_length**2, system_length**2))

bss_env = BSS_Env_Init(description, steps, system_length, user_hourly_distrib, supply_distrib, arrival_distrib, destinations_distrib)

# Serialize BSS Init object
pkl.dump(bss_env, open("DC_base.pkl", 'wb+'))
