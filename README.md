# Social champion identification

Identifying a social champion using the concepts of natural language processing

### Requirements

* Python 3.5 or above
* Anaconda / Miniconda
* Elasticsearch

### Dependency Installation

Create a new conda environment and activate it

```sh
conda create --name sci
activate sci
```

Install dependencies

```sh
$ pip install -r requirements.txt
$ python -m spacy download en
$ python -m nltk.downloader stopwords
```



### Starting the environment

First start your elasticsearch server

```sh
$ python api.py
```
  