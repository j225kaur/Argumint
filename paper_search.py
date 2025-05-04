import requests
def search_papers(query, limit=3):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&fields=title,abstract,authors,url"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch papers:", response.status_code)
        return []

    data = response.json()
    papers = []

    for paper in data.get("data", []):
        abstract = paper.get("abstract")
        if not abstract:
            continue  # Skip papers with no abstract

        papers.append({
            "title": paper.get("title", "No title"),
            "abstract": abstract,
            "authors": ", ".join(a.get("name", "") for a in paper.get("authors", [])),
            "url": paper.get("url", "")
        })

    return papers

