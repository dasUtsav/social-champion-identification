import re
import json
from pprint import pprint as pp

class text_retrieve:
    noise_list =  ['is','the','am','a','to','us','on','I','and','by','etc.','all','&','an','all.','A','have','has','had','in','most','of','your','.',',','are']
    #d1 and d2 are of type dictionary whereas data is of type list ........
    ##################Step one for data cleansing ###################
    def noise_removal(self,data):
        
        for d in data:
            for d1 in d['data']:# itering through the list of dictionary
                words = d1['message'].split()
                noise_free_Wordlist = []
                for word in words:
                    if word not in self.noise_list:
                        noise_free_Wordlist.append(word)
                d1['message'] = ' '.join(noise_free_Wordlist)
        return data
               
    #####Fetching callouts and hashtag in data cleansing ###################################
    
    def cal_hashTag_callout(self,data):
        hash_tag=[]
        callouts=[]
        for d in data:
            for d1 in d['data']:# itering through the list of dictionary
                words = d1['message'].split()#List of all the words 
                hash_tag.append([w.group(0) for word in words for w in re.finditer(r"#\w+", word)])
                callouts.append([word for word in words if re.search(r"^@[a-zA-Z0-9]+", word)])
        return callouts, hash_tag
        #hash_tag = [word for word in words if re.search(r'#\w+',word)]

with open('result.json') as data_file:
    data = json.load(data_file)
class_ref = text_retrieve()
sample_removal = class_ref.noise_removal(data)
callouts = class_ref.cal_hashTag_callout(data)
print(callouts)


    
    
    
    
    
    

