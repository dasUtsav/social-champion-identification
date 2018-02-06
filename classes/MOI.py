import numpy as np
import math
from copy import deepcopy

class MOI:
    def __init__(self, twitterGraph):
        self.twitterGraph = deepcopy(twitterGraph)

    def fetch_moi_score(self, screen_id, max_tweets):
        followers_count = self.twitterGraph.G.node[screen_id]['followers_count']
        favourites, retweets = self.twitterGraph.fetch_favourites(screen_id, max_tweets)
        favourites, retweets = np.array(favourites), np.array(retweets)
        roa = (favourites + retweets) / followers_count
        moi = np.linalg.norm(roa, 2) / (math.sqrt(len(roa)))
        return moi
