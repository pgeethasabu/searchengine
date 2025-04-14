from preprocess import preprocess_arxiv_json
from elastic_utils import connect_elasticsearch, create_index, index_data, bm25_search
from colbert_reranker import rerank

def main():
    json_path = "data/arxiv-metadata-oai-snapshot.json"
    index_name = "arxiv-papers"
    query = "quantum entanglement"

    print("🔄 Preprocessing...")
    df = preprocess_arxiv_json(json_path, max_records=10000)

    print("🔗 Connecting to Elasticsearch...")
    es = connect_elasticsearch()

    print("🗂️ Creating index & indexing documents...")
    create_index(es, index_name)
    index_data(es, df, index_name)

    print(f"🔍 Searching for: '{query}' using BM25...")
    candidates = bm25_search(es, index_name, query, size=50)

    print("🤖 Re-ranking with ColBERT...")
    final_results = rerank(query, candidates[:20])

    print("\n📄 Final Results:")
    for i, doc in enumerate(final_results[:10]):
        print(f"Rank {i+1}: {doc['title']}")
        print(doc['summary'][:300] + "...\n" + "-"*80)

if __name__ == "__main__":
    main()
