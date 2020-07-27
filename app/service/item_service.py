from models.item_model import Payload
from models.item_model import Question

from haystack import Finder
from haystack.indexing.cleaning import clean_wiki_text
from haystack.indexing.utils import convert_files_to_dicts, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers

from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.dense import DensePassageRetriever
from haystack.retriever.dense import EmbeddingRetriever

import pandas as pd
import requests
import uuid
import torch

# import wandb
# wandb.init(project="entro-haystack")

cuda_available = torch.cuda.is_available()

document_store = ElasticsearchDocumentStore(host="35.188.203.27",
                                            username="elastic",
                                            password="qt5hfjmkmxtvlf4pw6qhlk6b",
                                            index="faq",
                                            text_field="answer",
                                            embedding_field="question_emb",
                                            embedding_dim=768,
                                            excluded_meta_data=["question_emb"])

retriever = EmbeddingRetriever(document_store=document_store, embedding_model="deepset/sentence_bert", use_gpu=cuda_available)

finder = Finder(reader=None, retriever=retriever)

def index_item(payload: Payload):

    item = payload.event.data.new

    df = pd.DataFrame({'id': item.id,'question': item.question, 'answer': item.answer, 'content': item.content}, index=[0])

    # Get embeddings for our questions from the FAQs
    questions = list(df["question"].values)
    df["question_emb"] = retriever.embed_queries(texts=questions)

    # Convert Dataframe to list of dicts and index them in our DocumentStore
    docs_to_index = df.to_dict(orient="records")
    document_store.write_documents(docs_to_index)

    return item

def ask_question(question: Question):
    print(question)

    prediction = finder.get_answers_via_similar_questions(question=question.question, top_k_retriever=10)

    return prediction