from gensim import corpora
from gensim.models import lsimodel

class LSIModeling:
    def train(self, texts, num_topics=5, num_words=10):
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        self.model = lsimodel.LsiModel(corpus, num_topics=num_topics, id2word = dictionary)
        self.topics = []
        for topic in self.model.print_topics(num_topics=num_topics, num_words=num_words):
            self.topics.append(topic)

