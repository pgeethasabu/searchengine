# Directory: retrieval/bm25_colbert.py

from elasticsearch import Elasticsearch
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

def connect_to_es():
    es = Elasticsearch("http://localhost:9200")
    if not es.ping():
        raise Exception("Elasticsearch not available")
    return es

def bm25_search(es, index_name, query, size=25):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "summary"]
            }
        }
    }
    results = es.search(index=index_name, body=body, size=size)
    hits = results["hits"]["hits"]
    return [{
        "id": hit["_id"],
        "title": hit["_source"]["title"],
        "summary": hit["_source"]["summary"]
    } for hit in hits]

def embed_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs).last_hidden_state
    return outputs.squeeze(0).mean(dim=0).numpy()

def colbert_rerank(query, docs):
    tokenizer = AutoTokenizer.from_pretrained("colbert-ir/colbertv2.0")
    model = AutoModel.from_pretrained("colbert-ir/colbertv2.0")
    model.eval()

    query_vec = embed_text(query, tokenizer, model)
    doc_vecs = [embed_text(doc["summary"], tokenizer, model) for doc in docs]
    scores = [np.dot(query_vec, dv) for dv in doc_vecs]
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked]
