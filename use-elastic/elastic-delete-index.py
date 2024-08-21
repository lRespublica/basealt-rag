import os
import argparse
import hashlib

from elasticsearch import Elasticsearch

username = 'elastic'
password = os.getenv('ELASTIC_PASSWORD') # Value you set in the environment variable
elasticAddr = os.getenv('ELASTIC_ADDR')

client = Elasticsearch(
    elasticAddr,
    basic_auth=(username, password)
)

client.indices.delete(index="clear_www.basealt.ru_rewrited")
