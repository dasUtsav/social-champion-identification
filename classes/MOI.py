import numpy as np
import math
from copy import deepcopy

class MOI:
    def __init__(self, twitterGraph):
        self.twitterGraph = deepcopy(twitterGraph)

    def fetch_moi_score(self, screen_id, max_tweets):
        followers_count = self.twitterGraph.G.node[screen_id]['followers_count']
        favorites, retweets = self.twitterGraph.fetch_favorites(screen_id, max_tweets)
        favorites, retweets = np.array([favorite['count'] for favorite in favorites]), np.array([0 if retweet['isRetweet'] else retweet['count'] for retweet in retweets])
        roa = (favorites + retweets) / followers_count
        moi = np.linalg.norm(roa, 2) / (math.sqrt(len(roa)))
        print(roa, moi)
        return moi
