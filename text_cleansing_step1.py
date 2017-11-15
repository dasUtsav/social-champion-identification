import re
import json

class text_retrieve:
    noise_list =  ['is','the','am','a','to','us','on','I','and','by','etc.','all','&','an','all.','A','have','has','had','in','most','of','your','.',',','are']

    def __init__(self, data):
        self.data = data
    #d1 and d2 are of type dictionary whereas data is of type list ........
    ##################Step one for data cleansing ###################
    def noise_removal(self):
        
        for d in self.data:
            for d1 in d['data']:# itering through the list of dictionary
                d1 = d1.__dict__
                words = d1['message'].split()
                noise_free_Wordlist = [word for word in words if word not in self.noise_list]
                d1['message'] = ' '.join(noise_free_Wordlist)
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


    
    
    
    
    
    

