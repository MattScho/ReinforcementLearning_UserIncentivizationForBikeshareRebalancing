'''
Generates a stream of users

:author: Matthew Schofield
'''
import numpy as np

class UserGenerator:

    def __init__(self):
        pass

    def distribution_generation(self, region_indices, users_for_hour, arrival_distrib, destination_distrib):
        output_users = []
        arrivals = np.random.choice(region_indices, users_for_hour, p=arrival_distrib)
        for a in arrivals:
            d = np.random.choice(region_indices, p=destination_distrib[a])
            output_users.append([a, d])
        return output_users
