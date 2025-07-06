import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from chatbot.live_search import crawl_site, model
import numpy as np

texts, urls = crawl_site()
embeddings = model.encode(texts, convert_to_numpy=True)
np.save("naic_embeddings.npy", embeddings)

with open("naic_texts.txt", "w") as f:
    for url, txt in zip(urls, texts):
        f.write(f"{url}\n{txt[:1000]}\n---\n")

print("Index built and saved.")
