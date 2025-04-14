from transformers import AutoTokenizer, AutoModel
import torch, numpy as np

tokenizer = AutoTokenizer.from_pretrained("colbert-ir/colbertv2.0")
model = AutoModel.from_pretrained("colbert-ir/colbertv2.0")
model.eval()

def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        output = model(**inputs).last_hidden_state
    return output.squeeze(0).mean(dim=0).numpy()

def rerank(query, documents):
    q_vec = embed_text(query)
    doc_vecs = [embed_text(doc["summary"]) for doc in documents]
    scores = [np.dot(q_vec, d_vec) for d_vec in doc_vecs]
    return [doc for _, doc in sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)]
