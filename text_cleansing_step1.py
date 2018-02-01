import re
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer
from twitter import Twitter

class Text_retrieve:
    #noise_list =  ['is','the','am','a','to','us','on','I','and','by','etc.','all','&','an','all.','A','have','has','had','in','most','of','your','.',',','are']
   
    def __init__(self, data):
        self.data = data
        self.en_stop = set(stopwords.words('english'))

    ##################Step one for data cleansing ###################
    def noise_removal(self):
        tokenized_words = []
        urlPattern = ""
        tokenizer = RegexpTokenizer(r'\w+')
        tweetTokenizer = TweetTokenizer(reduce_len=True)
        for d1 in self.data:
            if not isinstance(d1, dict):
                d1 = d1.__dict__
            message = d1['message'].lower()
            message = re.sub(r"http\S+","",message)
            message = re.sub(r"rt","",message)
            message = re.sub("(@[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)", " ", message)
            words = tokenizer.tokenize(message)            
            noise_free_Wordlist = [word for word in words if word not in self.en_stop
                                    or not re.search(r"^[^\w]$", word)]
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
            hash_tag.append([w.group(0) for word in words for w in re.finditer(r"#\w+", word)])
            callouts.append([word for word in words if re.search(r"^@[a-zA-Z0-9]+", word)])
        hash_tag = self.flatten2DArray(hash_tag)
        callouts = self.flatten2DArray(callouts)
        return callouts, hash_tag

    def lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        lemmatized = []
        noiseless_words = self.noise_removal()
        for message_tokens in noiseless_words:
            lemmatized_words = [lemmatizer.lemmatize(w) for w in message_tokens]
            lemmatized_words = [w for w in lemmatized_words]
            lemmatized.append(lemmatized_words)
        # lemmatized = self.flatten2DArray(lemmatized)
        return lemmatized



    
    
    
    
    
    

