import pandas as pd
import pickle
import numpy as np

class Ranking:
    def __init__(self, documents, topic_relevance):
        self.dataframe = {}
        self.dataframe['likes'] = [document['favourite_count'] for document in documents]
        self.dataframe['retweets'] = [document['retweet_count'] for document in documents]
        self.dataframe['isRetweet'] = [document['isRetweet'] for document in documents]
        self.dataframe['urls'] = [len(document['urls']) for document in documents]
        self.dataframe['hashtags'] = [len(document['hashtags']) for document in documents]
        self.dataframe['topic_relevance'] = topic_relevance.values.tolist()
        self.dataframe = pd.DataFrame(self.dataframe)
        scalerColumns = ['likes', 'retweets']
        with open('scaler.pickle', 'rb') as f:
            scaler = pickle.load(f)
        X_train_np = self.dataframe[scalerColumns].values
        X_train_np = scaler.transform(X_train_np)
        self.dataframe[scalerColumns] = X_train_np

    def rank(self):
        self.dataframe['rank'] = np.array(0.01*(self.dataframe['likes'] + self.dataframe['retweets'])
                                         + 0.2*(self.dataframe['hashtags'] + self.dataframe['urls']) 
                                         - 0.075*self.dataframe['isRetweet'] + 3*self.dataframe['topic_relevance'])