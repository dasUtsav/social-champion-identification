import facebook

from classes.Post import Post

access_token = "EAABZBfg9w4HgBAC58ta4cbc0ZBZA5HNmF6RPmu4IOjdnlnXz376iWUZCnIhXK9k5qmYOwjH5EeaTACmnRvGEGt97eKOVlZAkcFAIk4NIy729sagoVpt1Gr8qpkUXplEyj7ROt1wWTHrdNvRRUNg2Cyr5poFwZB7QjZAK1L8I2ACqefrLw4mHTbzZBJVHzCG9ZAqZBviQL8AjVanQZDZD"

# Initialize graph object
graph = facebook.GraphAPI(access_token=access_token, version="2.1")


def findInListDict(list, dictKey, value):
    for item in list:
        if item[dictKey] == value:
            return item

# Profile usernames
usernames = ['RUR.AreYouReducingReusingRecycling', 'EARTHOHOLICS']

pageDict = []

for username in usernames:
    pageDict.append({'name': username, 'data': []})
pageDict = sorted(pageDict, key=lambda page: page['name'].lower())


getPageLikes = graph.get_objects(ids=usernames, fields='feed{likes.summary(true), message}, fan_count')

for username in getPageLikes:
    item = findInListDict(pageDict, 'name', username)
    item['page_likes'] = getPageLikes[username]['fan_count']
    for data in getPageLikes[username]['feed']['data']:
        message = ""
        if('message' in data):
            message = data['message']
        item['data'].append(Post(data['id'], message, data['likes']['summary']['total_count']))
                            
for post in pageDict[1]['data']:
    print(post.postId)
        

