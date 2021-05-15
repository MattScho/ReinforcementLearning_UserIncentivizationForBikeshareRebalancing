'''
Data Structure to define BSS initializations

Schema
stepsPerEpisode = int (24)
systemLength = int (8)
user_hourly distribtion = [h1, h2, ..., hn] percentage of users per hour

supply = [r1, r2, ..., r100] len 100, where rn is a float for the probability of the bicycle starting at each region
TODO:
Supply distribution can be made more creatively, i.e. gen a static int supply matrix then apply a variable gaussian
noise matrix based on data

arrivals = [
    [a1_1, a1_2, ..., a1_n ],
     ...,
    [ah_1, ah_2, ..., ah_n]
], where h is hour and n is n regions, hourly probabilities per region for user arrival

destinations = [
    [
        [d1_1_1, d1_1_2, ..., d1_1_n],
        ...,
        [d1_a_1, d1_a_2, ..., d1_a_n]
    ],
    ...
    [
        [dh_1_1, dh_1_2, ..., dh_1_n],
        ...,
        [dh_a_1, dh_a_2, ..., dh_a_n]
    ]
], where h is hour, n is number of regions, a is arrival dest
Access dest[h][a] for the distribution to find destination region

description = str, description of the environment
'''
class BSS_Env_Init:

    def __init__(self, description, steps, system_length, users_per_hour, supply_ditrib, arrival_distribs, dest_distribs):
        # Steps per episode/game, aka number of hours
        self.steps = steps

        # Length of one side of the matrix (length of a vector within matrix),
        # the systems are square matrices, therefore systemLength^2 is the total number of elements in the
        # system
        self.system_length = system_length

        # Supply of bikes at each region
        self.supply_distrib = supply_ditrib

        # Arrival and destination distributions
        self.arrival_distribs = arrival_distribs
        self.dest_distribs = dest_distribs
        self.user_per_hour = users_per_hour

        # Add a description for init settings
        self.description = description

    def get_steps(self):
        return self.steps

    def get_init_supply(self):
        return self.supply_distrib

    def get_arrivals(self):
        return self.arrival_distribs

    def get_destinations(self):
        return self.dest_distribs

    def get_user_per_hour(self):
        return self.user_per_hour

    def get_system_length(self):
        return self.system_length

    def get_description(self):
        return self.description