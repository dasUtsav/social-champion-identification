import networkx as nx
import numpy as np
import json
from copy import deepcopy

config = json.load(open("config.json", 'r'))

class TopicInfluence:

    def __init__(self, twitterGraph):
        self.twitterGraph = twitterGraph

    def calcSimilarity(self, nodeId):
        doc = [[word for tweet in self.twitterGraph.G.node[nodeId]['tweet_doc'] 
              for word in tweet]]
        model, dictionary = self.twitterGraph.model, self.twitterGraph.dictionary
        follower_bow = [dictionary.doc2bow(text) for text in doc]
        for topic in model[follower_bow]:
            topicIndices = [a for (a, b) in topic]
            absentTopics = [i for i in range(0, 10) if i not in topicIndices]
            for topicIndex in absentTopics:
                self.twitterGraph.G.node[nodeId]['similarity'][topicIndex] = 0
            for (a, b) in topic:
                self.twitterGraph.G.node[nodeId]['similarity'][a] = b

    def compute_rank(self, max_tweets, center_nodes = [], gamma=1, force_fetch=False):
        candidate_ranks = []
        updated_center_nodes = list(center_nodes)
        print(center_nodes)
        if force_fetch is False:
            for center_node in center_nodes:
                if 'influence' in self.twitterGraph.G.node[center_node]:
                    candidate_ranks.append({
                        'node': center_node,
                        'influence': self.twitterGraph.G.node[center_node]['influence']
                    })
                    updated_center_nodes.remove(center_node)
        if len(updated_center_nodes) == 0:
            return candidate_ranks
        center_nodes = updated_center_nodes
        print("Length is not 0")
        node_array = self.getNodeArray(center_nodes)
        num_topics = config["topic_modeling"]["num_topics"]
        rank_vector_len = len(node_array)
        final_rank_vector = np.array([0 for a in range(0, rank_vector_len)])
        for topic_number in range(0, num_topics):
            probab_matrix = self.getProbabMatrix(max_tweets, center_nodes=center_nodes, node_array=node_array, topic_number=topic_number)
            rank_vector = np.array([1 for a in range(0, rank_vector_len)])
            for i in range(1, 10):
                rank_vector = gamma * np.dot(probab_matrix, rank_vector)
            final_rank_vector = final_rank_vector + rank_vector
        for center_node in center_nodes:
            index = node_array.index(center_node)
            candidate_ranks.append({
                'node': center_node,
                'influence': final_rank_vector[index]
            })
        return candidate_ranks

    def getNodeArray(self, center_nodes=[]):
        node_array = [node for center_node in center_nodes 
                      for (node, friend) in self.twitterGraph.G.in_edges(center_node)]
        node_array = list(set(node_array))
        node_array = list(node_array + center_nodes)
        return node_array

    def getProbabMatrix(self, max_tweets, topic_number , node_array,center_nodes = []):
        probab_matrix = []
        neighSumDict = {}

        for node in node_array:
            self.twitterGraph.set_tweet_doc(node, max_tweets)
            neighSum = 0
            for (ownNode, neighbor) in self.twitterGraph.G.edges(node):
                neighSum = neighSum + self.twitterGraph.G.node[neighbor]['status_count']
            neighSumDict[node] = neighSum

        for node1 in node_array:
            if node1 not in center_nodes:
                probab_vector = [0 if node != node1 else 1 for node in node_array]
                probab_matrix.append(probab_vector)
                continue
            probab_vector = []
            self.twitterGraph.set_model(node1, max_tweets, fetchTweetDoc=False)
            self.calcSimilarity(node1)
            for node2 in node_array:
                if node1 == node2:
                    score = 1
                elif self.twitterGraph.G.has_edge(node2, node1) and len(self.twitterGraph.G.node[node2]['tweet_doc']) != 0:
                    self.calcSimilarity(node2)
                    result = abs(self.twitterGraph.G.node[node1]['similarity'][topic_number] - self.twitterGraph.G.node[node2]['similarity'][topic_number])
                    score = self.twitterGraph.G.node[node1]['status_count'] / neighSumDict[node2] * (1 - result)
                else:
                    score = 0
                probab_vector.append(score)

            # neighSum = 0
            # for (ownNode, neighbor) in self.twitterGraph.G.edges(node1):
            #     neighSum = neighSum + self.twitterGraph.G.node[neighbor]['status_count']
            # probab_vector = []
            # for node2 in node_array:
            #     if node1 == node2:
            #         score = 1
            #     elif node2 in center_nodes and self.twitterGraph.G.has_edge(node1, node2) and len(self.twitterGraph.G.node[node1]['tweet_doc']) != 0:
            #         self.twitterGraph.set_model(node2, max_tweets, fetchTweetDoc=False)
            #         self.calcSimilarity(node2)
            #         self.calcSimilarity(node1)
            #         score = self.twitterGraph.G.node[node2]['status_count'] / neighSum * (1 - abs(self.twitterGraph.G.node[node1]['similarity'][topic_number] - self.twitterGraph.G.node[node2]['similarity'][topic_number]))
            #     else:
            #         score = 0
            #     probab_vector.append(score)
            probab_matrix.append(probab_vector)

        return np.array(probab_matrix)

