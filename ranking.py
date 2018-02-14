import pandas as pd
import pickle
import numpy as np
from scipy.stats import percentileofscore

class Ranking:
    def __init__(self, ranks, filters = ['influence', 'moiScore', 'topic_relevance']):
        self.filters = filters
        self.dataframe = pd.DataFrame(ranks)
        for filter in self.filters:
            self.dataframe = self.normalize(self.dataframe, filter)

    @staticmethod
    def normalize(df, column):
        df = pd.DataFrame(df)
        max = df[column].max()
        min = df[column].min()
        if max == 0:
            df[column] = 0
        else:
            df[column] = (df[column] - min) / (max - min)
        return df

    def rank(self, weightages):
        rank = []
        self.dataframe['rank'] = 0
        for filter in self.filters:
            self.dataframe['rank'] += self.dataframe[filter] * weightages[filter]
        self.dataframe = self.dataframe.sort_values(['rank'], ascending=0)
        dataFrameList = self.dataframe['rank'].tolist()
        self.percentileOfLast = percentileofscore(dataFrameList, dataFrameList[4])
        print("last percentile", self.percentileOfLast)