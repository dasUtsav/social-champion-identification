import pandas as pd
import pickle
import numpy as np

class Ranking:
    def __init__(self, documents, topic_relevance, sentiment):
        self.dataframe = {}
        self.dataframe['likes'] = [document['favourite_count'] for document in documents]
        self.dataframe['retweets'] = [document['retweet_count'] for document in documents]
        self.dataframe['isRetweet'] = [document['isRetweet'] for document in documents]
        self.dataframe['urls'] = [len(document['urls']) for document in documents]
        self.dataframe['hashtags'] = [len(document['hashtags']) for document in documents]
        self.dataframe['topic_relevance'] = topic_relevance.values.tolist()
        self.dataframe['sentiment'] = sentiment
        self.dataframe = pd.DataFrame(self.dataframe)
        nullValues = {'likes': 0, 'retweets': 0, 'isRetweet': 0, 'urls': 0,
                      'hashtags': 0, 'topic_relevance': -1}
        self.dataframe = self.dataframe.fillna(nullValues)
        scalerColumns = ['likes', 'retweets']
        with open('scaler.pickle', 'rb') as f:
            scaler = pickle.load(f)
        X_train_np = self.dataframe[scalerColumns].values
        X_train_np = scaler.transform(X_train_np)
        self.dataframe[scalerColumns] = X_train_np
        self.maxweight = 2
            

    def rank(self, filters=['topic_relevance', 'hashtags', 'urls', 'sentiment', 'likes', 'retweets', 'isRetweet']):
        weightages = {}
        rank = []
        for filter in filters:
            weightages[filter] = self.maxweight
            self.maxweight /= 2
        weightages['isRetweet'] = -0.075
        for filter in filters:
            rank.append(weightages[filter] * self.dataframe[filter])
        rank = np.asarray(rank)
        rank = np.sum(rank, axis=0)
        self.dataframe['rank'] = rank