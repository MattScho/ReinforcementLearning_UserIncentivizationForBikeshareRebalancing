import numpy as np
from environment.bss_controller_SADUE_A import BSS_Controller_SADUE_A

class BSS_Controller_Base_Direction(BSS_Controller_SADUE_A):


    def __init__(self, system_init_obj, budget, number_of_users, supply, games_file, steps_file):
        """
        Initializes the environment
        """
        super().__init__(system_init_obj, budget,number_of_users, supply, games_file, steps_file)

    '''
    Helper methods
    '''
    def step(self, action):
        # Get number of users for the hour
        users_for_hour = int(self.users * self.users_per_hour[self.curStep])

        arrival_distrib = self.arrival_distribution[self.curStep]
        destination_distrib = self.destination_distribution[self.curStep]

        # Record number of serviced and unserviced users (redundancy)
        serviced_users = 0
        unserviced_users = 0

        potential_unserviced_users = 0
        resolved_users = 0

        arrivals_mat = np.zeros(100)
        dest_mat = np.zeros(100)

        users = self.user_generator.distribution_generation(self.region_indices, users_for_hour, arrival_distrib,
                                                            destination_distrib)

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
                utilities = [(action[n] - self.walkingCost(), n) for n in neighbors]

                # Find 'best' move
                maxNeighbor = -1
                maxUtil = -1
                for u, n in utilities:
                    if u > maxUtil and self.S[n] > 0:
                        maxUtil = u
                        maxNeighbor = n

                # Check that the move is acceptable
                if maxUtil >= 0 and self.budget >= action[maxNeighbor]:
                    # Service
                    self.D[d] += 1
                    self.A[maxNeighbor] += 1
                    self.S[maxNeighbor] -= 1
                    self.budget -= action[maxNeighbor]
                    self.E[a] += action[maxNeighbor]

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
