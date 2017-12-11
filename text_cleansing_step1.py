import re
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

class text_retrieve:
    #noise_list =  ['is','the','am','a','to','us','on','I','and','by','etc.','all','&','an','all.','A','have','has','had','in','most','of','your','.',',','are']
   
    def __init__(self, data):
        self.data = data
    #d1 and d2 are of type dictionary whereas data is of type list ........
    en_stop = set(stopwords.words('english'))
    ##################Step one for data cleansing ###################
    def noise_removal(self):
        
        for d in self.data:
            for d1 in d['data']:# iterating through the list of dictionary
                d1 = d1.__dict__
                words = d1['message'].lower().split()
                noise_free_Wordlist = [word for word in words if word not in self.en_stop]
                d1['message'] = ' '.join(noise_free_Wordlist)
                print(d1['message'])
        return self.data

    def flatten2DArray(self, array):
        return [j for i in array for j in i]
               
    #####Fetching callouts and hashtag in data cleansing ###################################
    
    def cal_hashTag_callout(self):
        hash_tag=[]
        callouts=[]
        for d in self.data:
            for d1 in d['data']:# itering through the list of dictionary
                d1 = d1.__dict__
                words = d1['message'].split()#List of all the words 
                hash_tag.append([w.group(0) for word in words for w in re.finditer(r"#\w+", word)])
                callouts.append([word for word in words if re.search(r"^@[a-zA-Z0-9]+", word)])
        hash_tag = self.flatten2DArray(hash_tag)
        callouts = self.flatten2DArray(callouts)
        return callouts, hash_tag

    def lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        lemmatized = []
        for d in self.data:
            for d1 in d['data']:
                d1 = d1.__dict__
                message_tokens = nltk.word_tokenize(d1['message'])
                lemmatized.append(lemmatizer.lemmatize(w) for w in message_tokens)
        lemmatized = self.flatten2DArray(lemmatized)
        return lemmatized


<<<<<<< Updated upstream
=======


>>>>>>> Stashed changes

    
    
    
    
    
    

