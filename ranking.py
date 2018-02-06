import pandas as pd
import pickle
import numpy as np

class Ranking:
    def __init__(self, ranks):
        self.dataframe = pd.DataFrame(ranks)

    def rank(self, filters=['influence', 'moiScore']):
        weightages = {}
        rank = []
        self.dataframe['rank'] = 0
        for filter in filters:
            weightages[filter] = 1 / 3
            self.dataframe['rank'] += self.dataframe[filter] * weightages[filter]
        
        print(self.dataframe)