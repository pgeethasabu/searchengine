from elasticsearch import Elasticsearch, helpers

def connect_elasticsearch():
    es = Elasticsearch("http://localhost:9200")
    if not es.ping():
        raise Exception("Elasticsearch not running at localhost:9200")
    return es

def create_index(es, index_name):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    es.indices.create(index=index_name, body={
        "settings": {"number_of_shards": 1},
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "summary": {"type": "text"},
                "authors": {"type": "text"},
                "categories": {"type": "keyword"},
                "published": {"type": "date"}
            }
        }
    })

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

def bm25_search(es, index_name, query, size=100):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "summary"]
            }
        }
    }
    return [hit["_source"] for hit in es.search(index=index_name, body=body, size=size)["hits"]["hits"]]
