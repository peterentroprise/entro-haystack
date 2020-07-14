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

document_store = ElasticsearchDocumentStore(host="35.202.130.14", username="", password="", index="item", text_field="answer", embedding_field="question_emb", embedding_dim=768, excluded_meta_data=["question_emb"])

retriever = EmbeddingRetriever(document_store=document_store, embedding_model="sentence_bert", gpu=cuda_available)

def index_item(item: Item):
    print(item)

    # Get dataframe with columns "question", "answer" and some custom metadata
    df = pd.read_csv("faq_covidbert.csv")
    
    # Minimal cleaning
    df.fillna(value="", inplace=True)
    df["question"] = df["question"].apply(lambda x: x.strip())
    print(df.head())

    # Get embeddings for our questions from the FAQs
    questions = list(df["question"].values)
    df["question_emb"] = retriever.embed_queries(texts=questions)

    # Convert Dataframe to list of dicts and index them in our DocumentStore
    docs_to_index = df.to_dict(orient="records")
    # add UUID to dict
    dicts_with_uuid = [dict(item, _id=str(uuid.uuid4())) for item in docs_to_index]
    # add UUID to dict
    dicts_with_uuid_and_type = [dict(item, _type="item") for item in dicts_with_uuid]

    # write docs to store
    document_store.write_documents(dicts_with_uuid_and_type)

    return dicts_with_uuid_and_type

def ask_question(question: Question):
    print(question)
    
    finder = Finder(reader=None, retriever=retriever)
    prediction = finder.get_answers_via_similar_questions(question="How is the virus spreading?", top_k_retriever=1)
    print_answers(prediction, details="all")

    return prediction