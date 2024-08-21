import os
import argparse
import hashlib

from elasticsearch import Elasticsearch
from langchain_community.document_loaders import DirectoryLoader, BSHTMLLoader
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

ollama_url = "http://10.4.128.81:11434"
oembed = OllamaEmbeddings(base_url=ollama_url, model="nomic-embed-text")

username = 'elastic'
password = os.getenv('ELASTIC_PASSWORD') # Value you set in the environment variable
elasticAddr = os.getenv('ELASTIC_ADDR')

siteName = "clear_www.basealt.ru_rewrited"

vectorstore = ElasticsearchStore(
    es_url=elasticAddr,
    index_name=siteName,
    embedding=oembed,
    es_user=username,
    es_password=password,
)

ollama = Ollama(
    base_url=ollama_url,
    model="llama3.1"
)


questions = [
    "Что такое Альт Линукс?",
    "Кто разрабатывает Альт Линукс?",
    "Какие продукты выпускает Базальт СПО?",
    "Разрабатывает ли Базальт СПО продукты, связанные с виртуализацией?",
    "Что такое ALT Linux Team",
    "Что входит в состав Альт Сервера Виртуализации?",
    "Что такое групповые политики?",
    "Есть ли Kubernetes в составе Альт СП?",
]

DEBUG = None

for question in questions:
    print("\n>>> " + question)
    docs = vectorstore.similarity_search(query=question, k=6)

    if DEBUG:
        for d in docs:
            print("\n>>> " + question, file=sys.stderr)
            print(d.metadata, file=sys.stderr)
            print(d.page_content, file=sys.stderr)
            print("", file=sys.stderr)

    qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
    res = qachain.invoke({"query": question})
    print("Ответ:\n")
    print(res['result'])
    print()
