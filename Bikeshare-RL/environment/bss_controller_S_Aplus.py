from gym import spaces
import numpy as np
from environment.bss_controller_base_direction import BSS_Controller_Base_Direction

class BSS_Controller_S_Aplus(BSS_Controller_Base_Direction):
    '''
    Author Matthew Schofield
    Version 3.8.2021

    Reduced state space to only supply
    '''

    def __init__(self, systemInitObj, budget, number_of_users, supply, games_file, steps_file):
        """
        Initializes the environment
        """
        super().__init__(systemInitObj, budget, number_of_users, supply, games_file, steps_file)

        # OpenAi Gym settings
        self.action_space = spaces.Box(0, 5, shape=(self.system_length**2,), dtype=np.float32)
        self.observation_space = spaces.Box(0.0, 100.0, shape=(self.system_length**2,), dtype=np.float32)

    '''
    Helper methods
    '''
    def buildState(self):
        state = self.S
        return state