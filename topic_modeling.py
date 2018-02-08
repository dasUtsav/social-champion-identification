import json
import pandas as pd
import pickle
from gensim import corpora
from gensim.models import ldamodel
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from text_cleansing_step1 import Text_retrieve
from textblob import TextBlob

config = json.load(open("config.json", 'r'))
elasticConfig = config['elasticsearch']

class LDAModeling:

    def __init__(self, filename):
        self.filename = filename

    def train(self, texts, num_topics=5, num_words=10, num_passes=1):
        self.dictionary = corpora.Dictionary(texts)
        corpus = [self.dictionary.doc2bow(text) for text in texts]
        self.model = ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = self.dictionary, passes=num_passes)
        self.topics = []
        self.num_topics = num_topics
        self.num_words = num_words
        for topic in self.model.print_topics(num_topics=num_topics, num_words=num_words):
            self.topics.append(topic)

    def update(self, texts):
        self.dictionary.add_documents(texts)
        corpus = [self.dictionary.doc2bow(text) for text in texts]
        self.model.update(corpus)
        self.topics = []
        for topic in self.model.print_topics(num_topics=self.num_topics, num_words=self.num_words):
            self.topics.append(topic)     
    
    def index(self):
        config = json.load(open("config.json", 'r'))
        self.es = Elasticsearch([{'host': elasticConfig['host'], 'port': elasticConfig['port']}])
        index = elasticConfig['index']
        doc_type = elasticConfig['doc_type']
        if not self.es.indices.exists(index):
            print("creating index")
            for i in range(len(self.topics)):
                self.es.create(index=index, doc_type=doc_type, id=i+1, body={"content": str(self.topics[i])})

    def updateIndices(self):
        index = elasticConfig['index']
        doc_type = elasticConfig['doc_type']
        for i in range(len(self.topics)):
            self.es.update(index=index, doc_type=doc_type, id=i+1, body={"gg": "wp"})

    def deleteIndex(self):
        self.es = Elasticsearch([{'host': elasticConfig['host'], 'port': elasticConfig['port']}])
        esIndices = IndicesClient(self.es)
        index = elasticConfig['index']
        doc_type = elasticConfig['doc_type']
        esIndices.delete(index=index)

    def search(self, query, noOfResults=3):
        res = self.es.search(doc_type=elasticConfig['doc_type'], body={"query": {"match": {"content": query}}})
        if not res['hits']['hits']:
            return False
        id = [int(topic['_id']) for topic in res['hits']['hits']]
        return id[:noOfResults]

    def saveAsPickle(self):
        topic_model_list = [self.model, self.topics, self.dictionary, self.num_topics, self.num_words]
        with open(self.filename, 'wb') as pickleFile:
            pickle.dump(topic_model_list, pickleFile)
    
    def loadPickle(self):
        with open(self.filename, 'rb') as pickleFile:
            topic_model_list = pickle.load(pickleFile)
            self.model, self.topics, self.dictionary, self.num_topics, self.num_words = topic_model_list

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def getTopicDistFromQuery(self, docs, query):
        topic_ids = self.search(query)
        doc_topic_dist = self.topicDist(docs)
        print(doc_topic_dist)
        print(topic_ids)
        final_topic_dist = 0
        divisor = 1
        for topic in topic_ids:
            if topic in doc_topic_dist:
                final_topic_dist = doc_topic_dist[topic] / divisor
                break
            divisor *= 2

        return 0 if final_topic_dist is 0 else final_topic_dist.iloc[0]
    
    def topicDist(self, docs):
        # textAndNoise = Text_retrieve(docs)
        # lemmatized = textAndNoise.lemmatize()
        docs = [[word for tweet in docs 
              for word in tweet]]   
        doc_bow = [self.dictionary.doc2bow(text) for text in docs]
        doc_sample = []
        topicVar = {}
        for topic in self.model[doc_bow]:
            sample = [b for (a,b) in topic]
            doc_sample.append(sample)
            topicVar = topic

        doc_topic_dist = pd.DataFrame(doc_sample,columns=[a for (a,b) in topicVar])
        return doc_topic_dist



