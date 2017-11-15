import re
import json

class text_retrieve:
    
    with open('result.json') as data_file:
        data = json.load(data_file) 
    from pprint import pprint as pp
    
    noise_list =  ['is','the','am','a','to','us','on','I','and','by','etc.','all','&','an','all.','A','have','has','had','in','most','of','your','.',',','are']
    #d1 and d2 are of type dictionary whereas data is of type list ........
    ##################Step one for data cleansing ###################
    for d in data:
        for d1 in d['data']:# itering through the list of dictionary
            words = d1['message'].split()
            noise_free_Wordlist = []
            for word in words:
                if word not in noise_list:
                    noise_free_Wordlist.append(word)
            d1['message'] = ' '.join(noise_free_Wordlist)
            print(d1['message'])
            print()
    print()
    #####Fetching callouts and hashtag in data cleansing ###################################
    hash_tag=[]
    callouts=[]
    for d in data:
        for d1 in d['data']:# itering through the list of dictionary
            words = d1['message'].split()#List of all the words 
            hash_tag.append([w.group(0) for word in words for w in re.finditer(r"#\w+", word)] )
            callouts.append([word for word in words if re.search(r"^@[a-zA-Z0-9]+", word)] )
            #hash_tag = [word for word in words if re.search(r'#\w+',word)]

    print(hash_tag)
    print(callouts)

    
    
    
    
    
    

