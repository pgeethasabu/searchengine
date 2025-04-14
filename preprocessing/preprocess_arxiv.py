# Directory: preprocessing/preprocess_arxiv.py

import os
import json
import re
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm
import time

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def safe_date(date_str):
    try:
        return pd.to_datetime(date_str).isoformat()
    except Exception:
        return None

def preprocess_arxiv_json(json_file_path, max_records=None):
    records = []
    with open(json_file_path, 'r') as f:
        for i, line in enumerate(f):
            if max_records and i >= max_records:
                break
            try:
                entry = json.loads(line)
            except Exception:
                continue

            authors_list = entry.get('authors_parsed', [])
            authors = [f"{a[1]} {a[0]}" for a in authors_list if isinstance(a, list)]
            if not authors:
                authors = [entry.get("authors", "")]

            published = ""
            if isinstance(entry.get('versions'), list) and len(entry['versions']) > 0:
                published = entry['versions'][0].get('created', '')

            processed_entry = {
                'id': entry.get('id'),
                'submitter': entry.get('submitter', ''),
                'title': clean_text(entry.get('title', '')),
                'summary': clean_text(entry.get('abstract', '')),
                'authors': ', '.join(authors),
                'comments': entry.get('comments', ''),
                'journal_ref': entry.get('journal-ref', ''),
                'doi': entry.get('doi', ''),
                'report_no': entry.get('report-no', ''),
                'categories': entry.get('categories', ''),
                'license': entry.get('license', '') or '',
                'update_date': safe_date(entry.get('update_date', '')),
                'published': safe_date(published)
            }
            records.append(processed_entry)
    return pd.DataFrame(records)

def create_index(es, index_name):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    index_config = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "submitter": {"type": "text"},
                "title": {"type": "text"},
                "summary": {"type": "text"},
                "authors": {"type": "text"},
                "comments": {"type": "text"},
                "journal_ref": {"type": "text"},
                "doi": {"type": "keyword"},
                "report_no": {"type": "keyword"},
                "categories": {"type": "keyword"},
                "license": {"type": "keyword"},
                "update_date": {"type": "date"},
                "published": {"type": "date"}
            }
        }
    }
    es.indices.create(index=index_name, body=index_config)

def index_data(es, df, index_name):
    actions = [
        {
            "_index": index_name,
            "_id": row["id"],
            "_source": row.to_dict()
        }
        for _, row in df.iterrows()
    ]
    helpers.bulk(es, actions)

def connect_to_es():
    es = Elasticsearch("http://localhost:9200")
    if not es.ping():
        raise Exception("Elasticsearch not available")
    return es

def run_preprocessing():
    file_path = "data/arxiv-metadata-oai-snapshot.json"
    df = preprocess_arxiv_json(file_path, max_records=10000)
    es = connect_to_es()
    index_name = "arxiv-papers"
    create_index(es, index_name)
    index_data(es, df, index_name)
    print("✅ Preprocessing and Indexing Complete.")

if __name__ == "__main__":
    run_preprocessing()


