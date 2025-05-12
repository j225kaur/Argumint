import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def search_papers(query, limit=3, fetch_limit=15):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={fetch_limit}&fields=title,abstract,authors,url"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch papers:", response.status_code)
        return []

    data = response.json()
    raw_papers = [p for p in data.get("data", []) if p.get("abstract")]

    if not raw_papers:
        print("No papers found with abstracts.")
        return []

    abstracts = [p["abstract"] for p in raw_papers]
    texts = [query] + abstracts  
    if len(texts) < 2:
        return []

    vectorizer = TfidfVectorizer().fit_transform(texts)
    cosine_similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    scored_papers = []
    for score, paper in zip(cosine_similarities, raw_papers):
        scored_papers.append({
            "title": paper.get("title", "No title"),
            "abstract": paper.get("abstract", ""),
            "authors": ", ".join(a.get("name", "") for a in paper.get("authors", [])),
            "url": paper.get("url", ""),
            "score": score
        })

    scored_papers.sort(key=lambda x: x["score"], reverse=True)
    return scored_papers[:limit]
