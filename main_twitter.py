import os
from classes.TwitterGraph import TwitterGraph
from classes.TopicInfluence import TopicInfluence
from classes.MOI import MOI
from Instances import twitterInstance
from topic_modeling import LDAModeling


twitterGraph = TwitterGraph("twitterGraph.pickle")

# twitterGraph.add_candidate('nasw', 10, 5)

max_followers = 15
max_tweets = 10
max_follower_friends = 5

if os.path.isfile("twitterGraph.pickle"):
    twitterGraph.load_pickle()
else:
    twitterGraph.add_candidate('nasw', max_followers, max_follower_friends)

screen_names = ["nasw", "meganneiljourno", "laurakatebanks", "mike_salter"]

# for screen_name in screen_names:
#     twitterGraph.add_candidate(screen_name, max_followers, max_follower_friends)
## Run this if you wanna reset the db
# twitterGraph.resetRefetch()

## Run in order to reset the tweet_doc prop
# twitterGraph.reset_prop('tweet_doc', [])

topicInfluence = TopicInfluence(twitterGraph)

candidates = []

for screen_name in screen_names:
    res = twitterInstance.api.get_user(screen_name)
    candidates.append(res.id)

# ranks = topicInfluence.compute_rank(max_tweets, candidates)

# twitterGraph.reset_prop('tweet_doc', [])

# moi = MOI(twitterGraph)

# for candidate in candidates:
#     dictionary = filter(lambda rank: rank['node'] == candidate, ranks)
#     for dict in dictionary:
#         dict["moiScore"] = moi.fetch_moi_score(candidate, max_tweets)

# for rank in ranks:
#     twitterGraph.G.node[rank['node']]['moiScore'] = rank['moiScore']
#     twitterGraph.G.node[rank['node']]['influence'] = rank['influence']

# twitterGraph.write_pickle()

tweet_doc = twitterGraph.fetch_tweets(candidates[0], max_tweets)

ldamodel = LDAModeling("ldamodel.pickle")
ldamodel.loadPickle()

# ldamodel.train(tweet_doc, num_topics=10, num_passes=15)

# ldamodel.saveAsPickle()



