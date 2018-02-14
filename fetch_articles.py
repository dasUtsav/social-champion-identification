import codecs
import re
import json
import datetime
from newspaper import Article
from newsapi import NewsApiClient
from classes.utility import unixTimeSeconds


config = json.load(open("config.json", 'r'))

newsapiConfig = config["newsapi"]

newsapi = NewsApiClient(api_key=newsapiConfig["api_key"])

def fetch_from_article(url, filename):
    article = Article(url)
    try:
        article.download()
        article.parse()
        article_text = article.text
        article_text = re.sub(r"\[(.*?)]", "", article_text)
        article_text = re.sub(r"See also", "", article_text)
        article_text = re.sub(r"Main article:.*", "", article_text)
        article_text = re.sub(r"Photo\n", "", article_text)
        article_text = re.sub(r"\n+", "\n", article_text)
        with codecs.open('./articles/' + filename, 'w', 'utf-8') as f:
            f.write(article_text)
    except:
        print("Could not download file")

def fetch_article(query, maxFetch):
    all_articles = newsapi.get_everything(q=query,
                                      sources='cnn',
                                      sort_by='relevancy')
    articles_url = [article['url'] for article in all_articles['articles']]
    baseFileName = "-".join(query.split(" "))
    for i in range(0, maxFetch):
        timeStamp = str(unixTimeSeconds(datetime.datetime.now(), True))
        fetch_from_article(articles_url[i], baseFileName + "-" + timeStamp + ".txt")

# fetch_article("health care", 10)
# fetch_from_article("https://en.wikipedia.org/wiki/Sanitation", "sanitation.txt")
# fetch_from_article("https://en.wikipedia.org/wiki/Health_care", "health-care.txt")
# fetch_from_article("https://en.wikipedia.org/wiki/Child_abuse", "child-abuse.txt")
# fetch_from_article("https://en.wikipedia.org/wiki/Blood_donation", "blood-donation.txt")
# fetch_article("child abuse", 10)
# fetch_article("sanitation", 10)
# fetch_article("health care", 10)
# fetch_article("education", 10)
fetch_article("toilet", 10)