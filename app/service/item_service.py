from models.item_model import Item

from haystack import Finder
from haystack.indexing.cleaning import clean_wiki_text
from haystack.indexing.utils import convert_files_to_dicts, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.sparse import ElasticsearchRetriever

import uuid

# import wandb
# wandb.init(project="entro-haystack")

def index_haystack(item: Item):
    print(item)

    document_store = ElasticsearchDocumentStore(host="35.202.130.14", username="", password="", index="document")

    doc_dir = "data/article_txt_got"
    s3_url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"
    fetch_archive_from_http(url=s3_url, output_dir=doc_dir)

    dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
    dicts_with_uuid = [dict(item, _id=str(uuid.uuid4())) for item in dicts]
    dicts_with_uuid_and_type = [dict(item, _type="item") for item in dicts_with_uuid]
    document_store.write_documents(dicts_with_uuid_and_type)
    
    return item

def ask_haystack(item: Item):
    print(item)

    document_store = ElasticsearchDocumentStore(host="35.202.130.14", username="", password="", index="document")

    retriever = ElasticsearchRetriever(document_store=document_store)

    reader = FARMReader(model_name_or_path="trained-model", use_gpu=False, num_processes=1)

    finder = Finder(reader, retriever)

    prediction = finder.get_answers(question=item.question, top_k_retriever=10, top_k_reader=5)
    
    return prediction