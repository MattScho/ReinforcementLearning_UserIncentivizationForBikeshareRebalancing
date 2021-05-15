"""
v2

Reduced state space to supply and RB

author Matthew Schofield
version 3.8.2021
"""
from gym import spaces
import numpy as np
from environment.bss_controller_SADUE_A import BSS_Controller_SADUE_A

class BSS_Controller_S_A(BSS_Controller_SADUE_A):
    '''
    Author Matthew Schofield
    Version 3.8.2021

    Changes from paper:

    Reduced state space to only supply
    '''

    def __init__(self, systemInitObj, budget, number_of_users, supply,games_file, steps_file):
        """
        Initializes the environment
        """
        super().__init__(systemInitObj, budget, number_of_users, supply, games_file, steps_file)
        self.observation_space = spaces.Box(0.0, 100.0, shape=(self.system_length**2,), dtype=np.float32)

    '''
    Helper methods
    '''
    def buildState(self):
        state = self.S
        return state

