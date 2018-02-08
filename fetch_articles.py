from newspaper import Article
import codecs
import re

def fetch_from_article(url, filename):
    article = Article(url)
    article.download()
    article.parse()
    article_text = article.text
    article_text = re.sub(r"\[(.*?)]", "", article_text)
    article_text = re.sub(r"See also", "", article_text)
    article_text = re.sub(r"Main article:.*", "", article_text)
    with codecs.open('./articles/' + filename, 'w', 'utf-8') as f:
        f.write(article_text)

fetch_from_article("https://en.wikipedia.org/wiki/Health_care", "health-care-1.txt")