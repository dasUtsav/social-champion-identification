import json
import pandas as pd
from gensim import corpora
from gensim.models import ldamodel
from elasticsearch import Elasticsearch
from text_cleansing_step1 import Text_retrieve
from textblob import TextBlob

class LDAModeling:

    def train(self, texts, num_topics=5, num_words=10, num_passes=1):
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        self.model = ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=num_passes)
        self.topics = []
        for topic in self.model.print_topics(num_topics=num_topics, num_words=num_words):
            self.topics.append(topic)
    
    def index(self):
        config = json.load(open("config.json", 'r'))
        elasticConfig = config['elasticsearch']
        self.es = Elasticsearch([{'host': elasticConfig['host'], 'port': elasticConfig['port']}])
        index = elasticConfig['index']
        doc_type = elasticConfig['doc_type']
        if not self.es.indices.exists(index):
            print("creating index")
            for i in range(len(self.topics)):
                self.es.create(index=index, doc_type=doc_type, id=i+1, body={"content": str(self.topics[i])})

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
    
    def topicDist(self, docs):
        # textAndNoise = Text_retrieve(docs)
        # lemmatized = textAndNoise.lemmatize()
        docs = [[word for tweet in docs 
              for word in tweet]]
        doc_dictionary = corpora.Dictionary(docs)
        doc_bow = [doc_dictionary.doc2bow(text) for text in docs]
        doc_sample = []
        topicVar = {}
        for topic in self.model[doc_bow]:
            sample = [b for (a,b) in topic]
            doc_sample.append(sample)
            topicVar = topic

        doc_topic_dist = pd.DataFrame(doc_sample,columns=[a for (a,b) in topicVar])
        return doc_topic_dist



