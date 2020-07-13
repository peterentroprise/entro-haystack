from models.item_model import Item
from models.item_model import Question

from haystack import Finder
from haystack.indexing.cleaning import clean_wiki_text
from haystack.indexing.utils import convert_files_to_dicts, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.sparse import ElasticsearchRetriever
from haystack.retriever.dense import EmbeddingRetriever

import pandas as pd
import requests
import uuid
import torch

# import wandb
# wandb.init(project="entro-haystack")

cuda_available = torch.cuda.is_available()

def index_item(item: Item):
    print(item)

#    # Download
#     temp = requests.get("https://raw.githubusercontent.com/deepset-ai/COVID-QA/master/data/faqs/faq_covidbert.csv")
#     open('small_faq_covid.csv', 'wb').write(temp.content)

#     # Get dataframe with columns "question", "answer" and some custom metadata
#     df = pd.read_csv("small_faq_covid.csv")
#     # Minimal cleaning
#     df.fillna(value="", inplace=True)df["question"] = df["question"].apply(lambda x: x.strip())
#     print(df.head())

#     # Get embeddings for our questions from the FAQs
#     questions = list(df["question"].values)
#     df["question_emb"] = retriever.create_embedding(texts=questions)

#     # Convert Dataframe to list of dicts and index them in our DocumentStore
#     docs_to_index = df.to_dict(orient="records")
#     document_store.write_documents(docs_to_index)
    
    return item

def ask_question(question: Question):
    print(question)

    document_store = ElasticsearchDocumentStore(host="35.202.130.14", username="", password="", index="document")

    retriever = ElasticsearchRetriever(document_store=document_store)

    reader = FARMReader(model_name_or_path="trained-model", use_gpu=cuda_available, num_processes=1)

    finder = Finder(reader, retriever)

    answers = finder.get_answers(question=question.question, top_k_retriever=10, top_k_reader=5)
    
    return answers