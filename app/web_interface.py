from flask import Flask, render_template, request
from retrieval.bm25_colbert import connect_to_es, bm25_search, colbert_rerank
from reranking.rankt5_pagerank import rerank_with_rankt5, apply_pagerank

app = Flask(__name__)
es = connect_to_es()
INDEX_NAME = "arxiv-papers"

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form["query"]

        # Pipeline
        bm25_results = bm25_search(es, INDEX_NAME, query)
        colbert_results = colbert_rerank(query, bm25_results[:15])
        rankt5_results = rerank_with_rankt5(query, colbert_results[:10])
        final_results = apply_pagerank(rankt5_results)

        results = final_results

    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
