import json, re
import pandas as pd

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip()) if text else ""

def safe_date(date_str):
    try:
        return pd.to_datetime(date_str).isoformat()
    except Exception:
        return None

def preprocess_arxiv_json(json_file_path, max_records=10000):
    records = []
    with open(json_file_path, 'r') as f:
        for i, line in enumerate(f):
            if i >= max_records: break
            try:
                entry = json.loads(line)
            except Exception:
                continue

            authors = [f"{a[1]} {a[0]}" for a in entry.get('authors_parsed', []) if isinstance(a, list)]
            if not authors:
                authors = [entry.get("authors", "")]

            published = entry['versions'][0].get('created', '') if entry.get('versions') else ""

            records.append({
                'id': entry.get('id'),
                'title': clean_text(entry.get('title', '')),
                'summary': clean_text(entry.get('abstract', '')),
                'authors': ', '.join(authors),
                'categories': entry.get('categories', ''),
                'published': safe_date(published)
            })

    df = pd.DataFrame(records)
    return df[df['summary'].str.strip().astype(bool)]
