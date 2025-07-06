import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

CRAWL_DEPTH = 1
MAX_PAGES = 10
BASE_URL = "https://content.naic.org/"

def is_valid_url(url):
    parsed = urlparse(url)
    return "naic.org" in parsed.netloc

def extract_text(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        return " ".join([p.get_text(strip=True) for p in soup.find_all(['p', 'li'])])
    except Exception:
        return ""

def crawl_site(base_url=BASE_URL):
    visited, texts, urls = set(), [], []
    queue = [(base_url, 0)]

    while queue and len(visited) < MAX_PAGES:
        url, depth = queue.pop(0)
        if url in visited or depth > CRAWL_DEPTH:
            continue

        visited.add(url)
        text = extract_text(url)
        if len(text) > 300:
            texts.append(text)
            urls.append(url)

        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")
            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if is_valid_url(next_url) and next_url not in visited:
                    queue.append((next_url, depth + 1))
        except:
            continue

    return texts, urls
