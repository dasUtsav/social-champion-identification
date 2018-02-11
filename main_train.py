import codecs
import spacy
from glob import glob
from text_cleansing_step1 import Text_retrieve
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from topic_modeling import LDAModeling
from gensim.models import Phrases

from configImports import topic_modeling


# from spacy.en import English

nlp = spacy.load("en")


def getTokenizedWords(filename):
    with codecs.open(filename, "r", "utf-8") as trainingFile:
        trainingText = trainingFile.read()
    doc = nlp(trainingText)
    texts, article = [], []
    for w in doc:
        if w.text != '\n' and not w.is_stop and not w.is_punct and not w.like_num:
            article.append(w.lemma_)
        if w.text == '\n':
            texts.append(article)
            article = []
    return texts

def create_bigram(texts, word1, word2):
    count = 0
    for textSent in texts:
        word = ""
        index = -1
        for i, text in enumerate(textSent):
            if text == word1:
                word = word2
                index = i
                continue
            elif word == text:
                count += 1
                textSent[index] = word1 + "_" + word2
                del textSent[i]
            word, index = "", -1

ldamodel = LDAModeling("ldamodel.pickle")
ldamodel.loadPickle()

def trainModel():
    articles = glob("./articles/*.txt")
    final_texts = []
    for article in articles:
        texts = getTokenizedWords(article)
        bigram = Phrases(texts)
        texts = [bigram[line] for line in texts]
        final_texts += texts
    ldamodel.update(final_texts)
    ldamodel.index()
    ldamodel.deleteIndex()
    ldamodel.index()
    ldamodel.saveAsPickle()

# trainModel()
ldamodel.index()
ldamodel.search("health care")

# ldamodel.saveAsPickle()
# print(ldamodel.topics)