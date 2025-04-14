# Directory: reranking/rankt5_pagerank.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import networkx as nx

def rerank_with_rankt5(query, documents, top_k=10):
    model_name = "castorini/monot5-base-msmarco"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.eval()

    inputs = [f"Query: {query} Document: {doc['title']} {doc['summary']} Relevant:" for doc in documents]
    tokens = tokenizer(inputs, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model.generate(**tokens, max_new_tokens=1)

    ranked = sorted(zip(documents, outputs), key=lambda x: -x[1][0].item())
    return [doc for doc, _ in ranked[:top_k]]

def build_citation_graph(documents):
    G = nx.DiGraph()
    for doc in documents:
        doc_id = doc['id']
        citations = doc.get("citations", [])  # You must have citation data
        for cited_id in citations:
            G.add_edge(doc_id, cited_id)
    return G

def apply_pagerank(documents):
    G = build_citation_graph(documents)
    pr_scores = nx.pagerank(G)
    return sorted(documents, key=lambda x: pr_scores.get(x['id'], 0), reverse=True)
