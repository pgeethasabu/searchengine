import pandas as pd
import igraph as ig
import json
import swifter
from tqdm import tqdm
from utils import safe_parse_references_grp23

# --- Config ---
csv_path_grp23 = "cleaned_arxiv_with_references_grp23.csv"
pagerank_csv_path_grp23 = "pagerank_scores_grp23.csv"
top_n_path_grp23 = "top_20_papers_by_pagerank_grp23.txt"
json_save_path_grp23 = "reference_load_grp23.json"
batch_size_grp23 = 10000

# --- Step 1: Optimized parsing helper ---
def fast_parse_or_empty_grp23(ref_grp23):
    if ref_grp23 == "[]" or not isinstance(ref_grp23, str):
        return []
    return safe_parse_references_grp23(ref_grp23)

# --- Step 2: Load and parse CSV in chunks ---
print("grp23 Loading CSV in chunks...")
reader_grp23 = pd.read_csv(csv_path_grp23, dtype={"id": str}, chunksize=batch_size_grp23, low_memory=False)
df_chunks_grp23 = []

for chunk_grp23 in tqdm(reader_grp23, desc="Parsing and collecting chunks"):
    chunk_grp23["references"] = chunk_grp23["references"].swifter.apply(fast_parse_or_empty_grp23)
    df_chunks_grp23.append(chunk_grp23)

print(f"before df_grp23:")
df_grp23 = pd.concat(df_chunks_grp23, ignore_index=True)
print(f"grp23 Total rows loaded: {len(df_grp23)}")

# --- Step 3: ID mappings from only actual paper IDs ---
print("grp23 Creating ID mappings...")
id_to_index_grp23 = {pid: idx for idx, pid in enumerate(sorted(df_grp23["id"]))}
index_to_id_grp23 = {idx: pid for pid, idx in id_to_index_grp23.items()}
print(f"grp23 Unique paper IDs mapped: {len(id_to_index_grp23)}")

# --- Step 4: Build citation edges ---
print("grp23 Building citation edges...")
edges_grp23 = []
get_idx_grp23 = id_to_index_grp23.get
append_edge_grp23 = edges_grp23.append

for row_grp23 in tqdm(df_grp23.itertuples(index=False), total=len(df_grp23)):
    citing_idx_grp23 = get_idx_grp23(row_grp23.id)
    if isinstance(row_grp23.references, list):
        for cited_id_grp23 in row_grp23.references:
            cited_idx_grp23 = get_idx_grp23(str(cited_id_grp23))
            if citing_idx_grp23 is not None and cited_idx_grp23 is not None:
                append_edge_grp23((cited_idx_grp23, citing_idx_grp23))

print(f"grp23 Total citation edges: {len(edges_grp23)}")

# --- Step 5: Compute PageRank ---
print("grp23 Computing PageRank using igraph...")
graph_grp23 = ig.Graph(directed=True)
graph_grp23.add_vertices(len(id_to_index_grp23))
graph_grp23.add_edges(edges_grp23)
pagerank_scores_grp23 = graph_grp23.pagerank(directed=True)

pagerank_df_grp23 = pd.DataFrame({
    "id": [index_to_id_grp23[i] for i in range(len(pagerank_scores_grp23))],
    "pagerank_score": pagerank_scores_grp23
})
print("grp23 pagerank_df_grp23")
pagerank_df_grp23.to_csv(pagerank_csv_path_grp23, index=False)
print(f"grp23 PageRank scores saved to: {pagerank_csv_path_grp23}")

# --- Step 6: Top 20 papers ---
top_n_grp23 = pagerank_df_grp23.sort_values("pagerank_score", ascending=False).head(20)
with open(top_n_path_grp23, "w", encoding="utf-8") as f:
    for _, row in top_n_grp23.iterrows():
        f.write(f"{row.id}\n")
print(f"grp23 Top 20 paper IDs saved to: {top_n_path_grp23}")

# --- Step 7: Optional JSON dump ---
print("grp23 Dumping reference JSON...")
with open(json_save_path_grp23, "w", encoding="utf-8") as jf:
    json.dump(df_grp23[["id", "original_title", "original_abstract", "references"]].to_dict(orient="records"), jf, indent=2)
print(f"grp23 JSON dump saved to: {json_save_path_grp23}")
