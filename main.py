# Directory: main.py

from preprocessing.preprocess_arxiv import run_preprocessing
from retrieval.bm25_colbert import connect_to_es, bm25_search, colbert_rerank
from reranking.rankt5_pagerank import rerank_with_rankt5, apply_pagerank

if __name__ == "__main__":
    query = input("🔍 Enter your search query: ")
    index_name = "arxiv-papers"

    print("Connecting to Elasticsearch...")
    es = connect_to_es()

    print("Retrieving with BM25...")
    bm25_results = bm25_search(es, index_name, query)

    print("Re-ranking with ColBERT...")
    colbert_results = colbert_rerank(query, bm25_results[:15])

    print("Refining with RankT5...")
    rankt5_results = rerank_with_rankt5(query, colbert_results[:10])

    print("Applying PageRank...")
    final_results = apply_pagerank(rankt5_results)

    print("\n📚 Final Results:")
    for i, doc in enumerate(final_results):
        print(f"\nRank {i+1}: {doc['title']}")
        print(doc['summary'][:300] + "...\n")
