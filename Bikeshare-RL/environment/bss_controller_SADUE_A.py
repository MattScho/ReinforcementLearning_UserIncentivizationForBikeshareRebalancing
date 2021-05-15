'''
V1

Spec detailed in class string

:author: Matthew Schofield
:version: 3.8.2021
'''
import gym
from gym import spaces
import numpy as np
from copy import deepcopy
import random
from environment.user_generator import UserGenerator

class BSS_Controller_SADUE_A(gym.Env):
    '''
    Implementation of a BikeShare Environment

    An environment inspired by the framework from the paper:
    A Deep Reinforcement Learning Framework for Rebalancing Dockless Bike Sharing Systems

    Original data could not be located so this environment will allow for distributions to be 'plugged-in'

    It should also be noted that the original paper relied on one month of Shanghai Mobike data
    Aug 1st - Sept 1st 2016.

    Paper Environment Implementation Summary:

    Definitions:
    Area n Regions: R={r1, r2, ..., rn}
    Day discretized into timeslots: T={t1, t2, ..., tm}
    N(ri) = ri's neighbors

    Si(t) = Supply in region ri at beginning of timeslot t
    S(t) = Vector of all region supplies at time t = (Si(t), {for all}i)
    Ai(t) = Arrivals in region ri at timeslot t
    A(t) = Vector of all region arrivals at time t = (Ai(t), {for all}i)
    Di(t) = Demand in region ri at timeslot t
    D(t) = Vector of all region demands at time t = (Di(t), {for all}i)
    dij(t) = Number of users intending to ride from region ri to region rj during timeslot t

    Pricing Algorithm:
    A - Agent - If a user arrives at ri in time tx and there are no bikes in ri the agent A can recommend bikes in N(ri)
        A will also give price incentive pij(t), offer at time t to move i to j
    B - Budget that the agent can use

    User Model:
    For all users in region ri, if there are available bikes they will take those. Otherwise apply walking cost model,
    ck(i,j,x) = { 0     i == j
                { ax^2  j in N(ri)
                { +inf  else
    uk(i, j, t, x) = utility of offer to user = pij(t) - ck(i,j,x)
    The user will take the max non-negative uk(i, j, t, x)
    If all uk's for the user are negative then the user's request is unsatisfied/"unserviced"


    Bike Flow Dynamics:
    Si(t+1) = Si(t) - (Bikes departed during t) + (Bikes arrived during t)

    Overall Goal:
    Optimize policy A to reduce BikeShare congestion given budget constraint B

    MDP Formulation:
    Definition -> (MDP_S, MDP_A, MDP_Pr, MRP_R, MDP_\gamma)
    MDP_S - States
    MDP_A - Actions
    MDP_Pr - Transition Matrix
    MDP_R - Reward
    MDP_\gamma - discount factor (standard RL \gamma) (they use .99)

    MDP_S = st = (S(t), D(t-1), A(t-1), E(t-1), RB(t), U(t))
        S(t) - (defined above) - Supply for each region
        D(t-1) - (defined above) - Demand for all regions at last timestep
        A(t-1) - (defined above) - Arrivals for all regions at last timestep
        E(t-1) - Expense at last timestep
        RB(t) - Remaining budget at timestep t
        U(t) - un-service ratio for each region for some number (not defined in paper) of past timesteps

    MDP_A = at = (p1t, ..., pnt) = price incentive for each region ! Their paper only offer 1 per region to leave from there !
    MDP_R = R(st, at) = ratio of satisfied requests at timestep t
    MDP_Pr = transition probability Pr(s_(t+1) | st,at) = probability st to s_(t+1) under action at

    policy pi_(\theta)(st) = maps current state to an action
    Objective find overall discounted rewards

    Data:
    User and Bike location within a region is drawn from a Uniform distribution
    They specify the initial system supply to be O x (3.65 / 20) where O is the number of orders in their system, however
        they do not specify a time frame and they do distribute bikes based on demand per region for which they do not
        provide data. I believe it is better to allow for varying supply and demand through a set distribution. I will
        generate layout files based on distributions and combinations there of, they will be placed in a directory
        BSS_Inits as .bssEnv files.

    State: Each region’s (Supply, Last Arrivals, Last Departures, Last Service Level, Last Expense)
    Action: Apply incentive to leave each region
    '''

    def __init__(self, bss_inits, budget, number_of_users, supply, games_file, steps_file):
        # Total number of regions
        """
        Initializes the environment

        :param bss_inits: Object to get system init parameters
        :param budget: budget for the game
        :param gamesFile: file to save agent learning progress by game to
        :param stepsFile: file to save agent learning progress by step to
        """
        # BSS Init parameters
        # System size (length across one dimension), systemSize = 10 means a 10x10 grid
        self.system_length = bss_inits.get_system_length()

        # Number of steps per episode
        self.steps = bss_inits.get_steps()

        self.users = number_of_users
        self.supply = supply

        # File to save step-wise learning progress
        self.step_file = steps_file

        # File to save game-wise learning progress
        self.games_file = games_file

        # Buffers to save outputs in
        self.games_file.write("Step,Number_of_Users,Serviced_Users,Unserviced_Users,Potential_Unserviced,Resolved,Budget\n")

        self.region_indices = np.arange(self.system_length ** 2)

        # Static Inits
        # Budget - the budget the agent has access to
        # S - Supply of bikes at each region, ie S[i] is current the supply at region i
        # A - Arrivals this timestep
        # D - Destinations this timestep
        # U - Unservice level this timestep
        # E - Expense for each region last timestep
        self.staticInits = {
            "Steps": self.steps,
            "Budget": budget,
            "S": np.multiply(bss_inits.get_init_supply(), supply),
            "A": np.zeros((self.system_length**2,)),
            "D": np.zeros((self.system_length**2,)),
            "U": np.zeros((self.system_length**2,)),
            "E": np.zeros((self.system_length**2,)),
            "TAij": bss_inits.get_arrivals(),
            "TDij": bss_inits.get_destinations(),
            "Nu": bss_inits.get_user_per_hour()
        }
        # Accumulators for performance
        self.accumulatedRew = 0
        self.serviceLevel = 0

        # OpenAi Gym settings
        self.action_space = spaces.Box(0, 5, shape=(self.system_length**2,), dtype=np.float32)
        self.observation_space = spaces.Box(0.0, 100.0, shape=(6, self.system_length**2,), dtype=np.float32)

        self.user_generator = UserGenerator()

        # Revert to original values
        self.revertToStaticInits()

    def getBudget(self):
        '''
        Getter for the game's budget

        :return: game budget
        '''
        return self.budget

    '''
    Gym top-levels
    '''
    def step(self, action):
        '''
        Take an action to impact the environment and receive feedback

        :param action: [incentive for all 100 regions]
        '''
        # Get number of users for the hour
        users_for_hour = int(self.users * self.users_per_hour[self.curStep])

        # Get distribution for arrivals
        arrival_distrib = self.arrival_distribution[self.curStep]

        # Get table of distributions for destinations
        destination_distrib = self.destination_distribution[self.curStep]

        # Record number of serviced and unserviced users (redundancy)
        serviced_users = 0
        unserviced_users = 0

        potential_unserviced_users = 0
        resolved_users = 0

        arrivals_mat = np.zeros(100)
        dest_mat = np.zeros(100)

        users = self.user_generator.distribution_generation(self.region_indices, users_for_hour, arrival_distrib, destination_distrib)

        for user in users:
            arrivals_mat[user[0]] += 1
            dest_mat[user[1]] += 1

        self.arrivals_buffer.append(np.divide(arrivals_mat, np.sum(arrivals_mat)))
        self.destinations_buffer.append(np.divide(dest_mat, np.sum(dest_mat)))

        # Iterate through users in the hour
        for user in users:
            # set users movement interest from arrival to destination
            a = user[0]
            d = user[1]

            # Check if we will need to service users
            if self.S[a] > 0:
                # Inc serviced users
                serviced_users += 1

                # Service record
                self.S[a] -= 1
                self.D[d] += 1
                self.A[a] += 1

            # Need to move the user
            else:
                # Inc may not be serviced
                potential_unserviced_users += 1

                # Move user
                neighbors = [n for n in self.neighbors(a) if n != -1]
                utilities = [(action[a] - self.walkingCost(), n) for n in neighbors]

                # Find 'best' move
                maxNeighbor = -1
                maxUtil = -1
                for u, n in utilities:
                    if u > maxUtil and self.S[n] > 0:
                        maxUtil = u
                        maxNeighbor = n

                # Check that the move is acceptable
                if maxUtil >= 0 and self.budget >= action[a]:
                    # Service
                    self.D[d] += 1
                    self.A[maxNeighbor] += 1
                    self.S[maxNeighbor] -= 1
                    self.budget -= action[a]
                    self.E[a] += action[a]

                    # Increment resolved and serviced
                    resolved_users += 1
                    serviced_users += 1
                else:
                    # Miss service
                    self.U[a] += 1

                    # Inc unserviced
                    unserviced_users += 1

        # Handles over head of state transition, users arrive
        self.resolvePreviousState()

        # Format output
        state = self.buildState()

        self.number_of_users += users_for_hour
        self.serviced_users += serviced_users
        self.unserviced_users += unserviced_users
        self.potential_unserviced_users += potential_unserviced_users
        self.resolved_users += resolved_users


        try:
            reduced_unservice_level = resolved_users / potential_unserviced_users
        except:
            reduced_unservice_level = 1.0

        # Check done
        done = self.curStep == self.steps
        info = {}

        return state, reduced_unservice_level, done, info

    def reset(self):
        '''
        Reset environment

        :return: New state
        '''
        # Write to game and step file
        self.games_file.write(
            str("%d,%d,%d,%d,%d,%d\n" %
                (
                    self.number_of_users, self.serviced_users, self.unserviced_users, self.potential_unserviced_users, self.resolved_users, self.budget)
                )
        )

        # Reset game
        self.revertToStaticInits()
        return self.buildState()

    def render(self, mode='human'):
        '''
        Render environment

        :param mode: changes representation method
            human -> print to terminal state representation
        '''
        print("Current Counts:")
        print(self.S)
        print(np.sum(self.S))
        print("State:")
        print(self.buildState())
        print("\n\n\n\n")

    def close(self):
        '''
        Clean up environment

        Rarely called
        '''
        self.step_file.close()
        self.games_file.close()
        print("Closed")

    '''
    Helper methods
    '''
    def buildState(self):
        state = np.array([
            self.S,
            self.A_1,
            self.D_1,
            self.U_1,
            self.E_1,
            np.full((self.system_length**2,), self.budget)
        ])
        return state

    def walkingCost(self):
        '''
        Calculate the walking cost from a user to a bike in a neighboring region

        :return: walking cost [0,4)
        '''
        # alpha parameter to adjust budget range
        alpha = 1.0
        userLoc = random.random()
        bikeLoc = 1 + random.random()

        return alpha * (bikeLoc - userLoc)**2

    def resolvePreviousState(self):
        '''
        Resolve previous state by finishing trips and moving
        array counters to the previous timestep
        '''
        # Resolve arrivals
        self.S = np.add(self.S, self.D)

        # Shift time window
        self.A_1 = deepcopy(self.A)
        self.D_1 = deepcopy(self.D)
        self.E_1 = deepcopy(self.E)
        self.U_1 = deepcopy(self.U)

        # Reset
        self.A = deepcopy(self.staticInits["A"])
        self.D = deepcopy(self.staticInits["D"])
        self.E = deepcopy(self.staticInits["E"])
        self.U = deepcopy(self.staticInits["U"])

        # Increment step counter
        self.curStep += 1

    def revertToStaticInits(self):
        '''
        Properly resetting the environment is one of the trickiest components in writing RL simulation software
        This routine helps to ensure proper memory management
        '''
        # This is only an int so it does not necessarily need a deepcopy, but this is not noticeably expensive
        # And adds resistance to future changes where Budget may be a 'real' Object
        self.budget = deepcopy(self.staticInits["Budget"])
        self.S = deepcopy(self.staticInits["S"])
        self.A = deepcopy(self.staticInits["A"])
        self.D = deepcopy(self.staticInits["D"])
        self.U = deepcopy(self.staticInits["U"])
        self.E = deepcopy(self.staticInits["E"])

        # A(t-1), D(t-1)
        self.A_1 = deepcopy(self.staticInits["A"])
        self.D_1 = deepcopy(self.staticInits["D"])
        self.U_1 = deepcopy(self.staticInits["U"])
        self.arrival_distribution = deepcopy(self.staticInits["TAij"])
        self.destination_distribution = deepcopy(self.staticInits["TDij"])
        self.users_per_hour = deepcopy(self.staticInits["Nu"])
        self.E_1 = deepcopy(self.staticInits["E"])

        self.number_of_users = 0
        self.serviced_users = 0
        self.unserviced_users = 0
        self.potential_unserviced_users = 0
        self.resolved_users = 0

        self.curStep = 0

        self.arrivals_buffer = []
        self.destinations_buffer = []

        for hour in range(21, 24):
            arrivals_mat = np.zeros(100)
            users_for_hour = int(self.staticInits["Nu"][hour] * self.users)
            arrivals = np.random.choice(self.region_indices, users_for_hour, p=self.staticInits["TAij"][hour])
            for a in arrivals:
                arrivals_mat[a] += 1
            self.arrivals_buffer.append(arrivals_mat)

        self.destinations_buffer.append(np.zeros(100))

    def neighbors(self, region_i):
        '''
        Outputs neighbors of index regionI

        :param region_i: index of region whose neighbors are to be found
        :return: [up, down, left, right]
        '''
        # Get length of rows, assumes square layout
        row_len = self.system_length

        # Calculate index of movement direction
        up = region_i - row_len
        down = region_i + row_len
        left = region_i - 1
        right = region_i + 1

        if up < 0:
            up = -1
        if down >= self.system_length**2:
            down = -1
        if left % row_len == row_len-1:
            left = -1
        if right % row_len == 0:
            right = -1

        return [int(up), int(down), int(left), int(right)]


