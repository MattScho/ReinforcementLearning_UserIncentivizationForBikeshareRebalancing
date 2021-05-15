from gym import spaces
import numpy as np
from environment.bss_controller_base_direction import BSS_Controller_Base_Direction
from environment.predictive_models.user_interest_predictor import UserInterestPredictor

class BSS_Controller_SApDp_Aplus(BSS_Controller_Base_Direction):
    '''
    Author Matthew Schofield
    Version 11.16.2020

    Changes from paper:

    Reduced state space to only supply
    '''

    def __init__(self, systemInitObj, budget, number_of_users, supply, games_file, steps_file):
        """
        Initializes the environment
        """
        super().__init__(systemInitObj, budget, number_of_users, supply, games_file, steps_file)

        # OpenAi Gym settings
        self.action_space = spaces.Box(0, 5, shape=(self.system_length**2,), dtype=np.float32)
        self.observation_space = spaces.Box(0.0, 100.0, shape=(3*self.system_length**2,), dtype=np.float32)

        self.model_connection = UserInterestPredictor()

        # Calculate prediction maps
        self.outgoing_prediction = {}
        self.incoming_prediction = {}


    '''
    Helper methods
    '''
    def buildState(self):
        state = self.S

        curStep = self.curStep
        if curStep == 24:
            curStep = 23

        inp = np.divide(self.arrivals_buffer[-3:], np.sum(self.arrivals_buffer[-3:]))

        distrib = self.model_connection.predict(np.array(inp))

        distrib = np.divide(distrib, np.sum(distrib))
        user_demand = np.multiply(distrib, self.users * self.users_per_hour[curStep])
        replenish = self.destinations_buffer[-1]

        state = np.array([state, replenish, user_demand])
        state = state.reshape((300))
        return state