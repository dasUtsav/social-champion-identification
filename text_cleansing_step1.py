import re
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class text_retrieve:
    #noise_list =  ['is','the','am','a','to','us','on','I','and','by','etc.','all','&','an','all.','A','have','has','had','in','most','of','your','.',',','are']
   
    def __init__(self, data):
        self.data = data
    #d1 and d2 are of type dictionary whereas data is of type list ........
    en_stop = set(stopwords.words('english'))
    ##################Step one for data cleansing ###################
    def noise_removal(self):
        tokenized_words = []
        for d in self.data:
            for d1 in d['data']:# iterating through the list of dictionary
                d1 = d1.__dict__
                words = nltk.word_tokenize(d1['message'].lower())
                noise_free_Wordlist = [word for word in words if word not in self.en_stop]
                tokenized_words.append(noise_free_Wordlist)
        return tokenized_words

    def flatten2DArray(self, array):
        return [j for i in array for j in i]
               
    #####Fetching callouts and hashtag in data cleansing ###################################
    
    def cal_hashTag_callout(self):
        hash_tag=[]
        callouts=[]
        noiseless_words = self.noise_removal()
        for words in noiseless_words:
            hash_tag.append([words[index+1] for index, w in enumerate(words) if w == "#"])
            callouts.append([words[index+1] for index, w in enumerate(words) if w == "@"])
        hash_tag = self.flatten2DArray(hash_tag)
        callouts = self.flatten2DArray(callouts)
        return callouts, hash_tag

    def lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        lemmatized = []
        noiseless_words = self.noise_removal()
        for message_tokens in noiseless_words:
            lemmatized.append(lemmatizer.lemmatize(w) for w in message_tokens)
        lemmatized = self.flatten2DArray(lemmatized)
        return lemmatized



    
    
    
    
    
    

