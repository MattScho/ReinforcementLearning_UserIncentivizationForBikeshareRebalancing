import numpy as np
import keras

'''
Wraps the user interest predictive model

:author: Matthew Schofield
:version: 4.28.2021
'''
class UserInterestPredictor:

    def __init__(self):
        '''
        Load in the model on intialization
        '''
        self.model = self.load_model()

    def load_model(self):
        '''
        This may be problematic due to absolute pathing, Good Luck!
        Read up on how absolute pathing works
        '''
        model = keras.models.load_model('../environment/predictive_models/model/arrival_pred.mdl')
        return model

    def format_user_interests(self, prev_user_interests):
        return np.array([prev_user_interests])

    def format_predicted_user_interest(self, prediction):
        return prediction[0]

    def predict(self, prev_user_interests):

        X = self.format_user_interests(prev_user_interests)

        y = self.format_predicted_user_interest(self.model.predict(X))
        return y

