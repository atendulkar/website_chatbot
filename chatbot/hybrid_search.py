import numpy as np
import faiss
from chatbot.live_search import crawl_site, model
from sklearn.metrics.pairwise import cosine_similarity
import re

PRE_INDEX = None
PRE_EMBEDDINGS = None
PRE_TEXTS = None

def split_into_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def load_preindexed_data():
    global PRE_INDEX, PRE_EMBEDDINGS, PRE_TEXTS
    if PRE_INDEX is None:
        PRE_EMBEDDINGS = np.load("naic_embeddings.npy")
        PRE_INDEX = faiss.IndexFlatL2(PRE_EMBEDDINGS.shape[1])
        PRE_INDEX.add(PRE_EMBEDDINGS)
        with open("naic_texts.txt", "r") as f:
            raw = f.read().split('---\n')
            PRE_TEXTS = [txt.strip() for txt in raw if txt.strip()]

def deduplicate_and_summarize(snippets, similarity_threshold=0.9, max_outputs=3):
    if not snippets:
        return "No results found."

    embeddings = model.encode(snippets, convert_to_numpy=True)
    selected = []
    used_indices = set()

    for i, emb in enumerate(embeddings):
        if i in used_indices:
            continue
        selected.append(snippets[i])
        sims = cosine_similarity([emb], embeddings)[0]
        for j, sim in enumerate(sims):
            if sim > similarity_threshold:
                used_indices.add(j)
        if len(selected) >= max_outputs:
            break

    return "\n\n".join(selected)

def hybrid_semantic_search(query, top_k=5):
    try:
        texts, urls = crawl_site()
        sentences = []
        sentence_sources = []

        for txt, url in zip(texts, urls):
            for sentence in split_into_sentences(txt):
                if len(sentence.split()) > 4:
                    sentences.append(sentence)
                    sentence_sources.append(url)

        if sentences:
            emb = model.encode(sentences, convert_to_numpy=True)
            index = faiss.IndexFlatL2(emb.shape[1])
            index.add(emb)
            query_emb = model.encode(query, convert_to_numpy=True).reshape(1, -1)
            D, I = index.search(query_emb, top_k)

            best = [f"{sentences[i]}\nSource: {sentence_sources[i]}" for i in I[0]]
            return deduplicate_and_summarize(best)
    except Exception as e:
        print("Live search failed:", e)

    load_preindexed_data()
    query_emb = model.encode(query, convert_to_numpy=True).reshape(1, -1)
    D, I = PRE_INDEX.search(query_emb, top_k)
    if D[0][0] < 1.0:
        best_snippets = [PRE_TEXTS[i] for i in I[0]]
        return deduplicate_and_summarize(best_snippets)
    return "Information not found."
