import networkx as nx
import numpy as np
from copy import deepcopy

class TopicInfluence:

    def __init__(self, twitterGraph):
        self.twitterGraph = deepcopy(twitterGraph)

    def calcSimilarity(self, nodeId):
        doc = [self.twitterGraph.G.node[nodeId]['tweet_doc']]
        model, dictionary = self.twitterGraph.model, self.twitterGraph.dictionary
        follower_bow = [dictionary.doc2bow(text) for text in doc]
        for topic in model[follower_bow]:
            topicIndices = [a for (a, b) in topic]
            absentTopics = [i for i in range(0, 10) if i not in topicIndices]
            for topicIndex in absentTopics:
                self.twitterGraph.G.node[nodeId]['similarity'][topicIndex] = 0
            for (a, b) in topic:
                self.twitterGraph.G.node[nodeId]['similarity'][a] = b

    def compute_rank(self, max_tweets, center_nodes = [], gamma=0.75):
        probab_matrix, node_array = self.getProbabMatrix(max_tweets, center_nodes)
        print(probab_matrix)
        rank_vector = np.array([1 for a in node_array])
        for i in range(1, 2):
            rank_vector = gamma * np.dot(probab_matrix.T, rank_vector)
        return rank_vector, node_array

    def getProbabMatrix(self, max_tweets, center_nodes = []):
        probab_matrix = []
        node_array = [node for center_node in center_nodes 
                      for (node, friend) in self.twitterGraph.G.in_edges(center_node)]
        node_array = list(set(node_array))
        for node in node_array:
            self.twitterGraph.set_tweet_doc(node, max_tweets)
        node_array = node_array + center_nodes
        for center_node in center_nodes:
            self.twitterGraph.set_model(center_node, max_tweets, setTweetDoc=True)
            self.calcSimilarity(center_node)
            for node1 in node_array:
                neighSum = 0
                for (ownNode, neighbor) in self.twitterGraph.G.edges(node1):
                    neighSum = neighSum + self.twitterGraph.G.node[neighbor]['status_count']
                probab_vector = []
                for node2 in node_array:
                    if node1 == node2:
                        score = 1
                    elif self.twitterGraph.G.has_edge(node1, node2) and len(self.twitterGraph.G.node[node1]['tweet_doc']) != 0:
                        self.calcSimilarity(node1)
                        score = self.twitterGraph.G.node[node2]['status_count'] / neighSum * (1 - abs(self.twitterGraph.G.node[node1]['similarity'][0] - self.twitterGraph.G.node[node2]['similarity'][0]))
                    else:
                        score = 0
                    probab_vector.append(score)
                probab_matrix.append(probab_vector)

        return np.array(probab_matrix), node_array

