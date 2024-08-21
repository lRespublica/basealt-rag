import os
import argparse
import hashlib

from elasticsearch import Elasticsearch
from langchain_community.document_loaders import DirectoryLoader, BSHTMLLoader
from langchain_elasticsearch import ElasticsearchStore
from langchain.embeddings import OllamaEmbeddings

ollama_url = "http://10.4.128.81:11434"
oembed = OllamaEmbeddings(base_url=ollama_url, model="nomic-embed-text")

username = 'elastic'
password = os.getenv('ELASTIC_PASSWORD') # Value you set in the environment variable
elasticAddr = os.getenv('ELASTIC_ADDR')

client = Elasticsearch(
    elasticAddr,
    basic_auth=(username, password)
)

def createParser():
    parser = argparse.ArgumentParser(
                    prog='ProcessBasealt',
                    description='The program allows you to extract all the content from a website',)

    parser.add_argument('dirPath')

    return parser

def main():
    args = createParser().parse_args()

    dirPath = args.dirPath

    if not os.path.isdir(dirPath):
        print(f"Directory {dirPath} does not exist")
        exit(1)

    if dirPath.endswith("/"):
        dirPath = dirPath[:-1]

    siteName = os.path.basename(dirPath)
    #pathToSite = os.path.dirname(dirPath)

    if not client.indices.exists(index=siteName):
        client.indices.create(index=(siteName))

    vector_store = ElasticsearchStore(
        es_url=elasticAddr,
        index_name=siteName,
        embedding=oembed,
        es_user=username,
        es_password=password,
    )

    data = []

    for d in os.walk(dirPath):
        loader = DirectoryLoader(d[0], glob="*.html",use_multithreading=True, loader_cls=BSHTMLLoader)
        data += loader.load()

    uuids = [hashlib.sha256(d.page_content.encode('utf-8')).hexdigest() for d in data]

    vector_store.add_documents(documents=data, ids=uuids)

if __name__ == "__main__":
    main()
