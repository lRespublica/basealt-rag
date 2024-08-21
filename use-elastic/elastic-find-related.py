import os
import elasticsearch_dsl

from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.embeddings import OllamaEmbeddings

ollama_url = "http://10.4.128.81:11434"
oembed = OllamaEmbeddings(base_url=ollama_url, model="nomic-embed-text")

username = 'elastic'
password = os.getenv('ELASTIC_PASSWORD') # Value you set in the environment variable
elasticAddr = os.getenv('ELASTIC_ADDR')

elastic_vector_search = ElasticsearchStore(
    es_url=elasticAddr,
    index_name="clear_www.basealt.ru_rewrited",
    embedding=oembed,
    es_user=username,
    es_password=password,
)

results = elastic_vector_search.similarity_search_with_score(
    query="Что такое Simply Linux?",
    k=4,
)
for res, score in results:
    print(res.metadata)
    print(score)
