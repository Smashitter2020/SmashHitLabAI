import os
import yaml
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

CONFIG_PATH = "config/model.yaml"
PROCESSED_DIR = "data/processed"
INDEX_DIR = "data/index"


def load_chunks():
    chunks = []
    metadatas = []

    for file in os.listdir(PROCESSED_DIR):
        if not file.endswith(".txt"):
            continue

        path = os.path.join(PROCESSED_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks.append(text)
        metadatas.append({"source": file})

    return chunks, metadatas


def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    embed_model_name = config["embeddings"]["model_name"]

    print(f"[load] Embedding model: {embed_model_name}")
    embedder = SentenceTransformer(embed_model_name)

    print("[load] Loading chunks...")
    chunks, metadatas = load_chunks()

    print("[embed] Encoding chunks...")
    embeddings = embedder.encode(chunks, show_progress_bar=True)

    print("[index] Creating Chroma index...")
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=INDEX_DIR))

    collection = client.get_or_create_collection(
        name="smash_hit_docs",
        metadata={"hnsw:space": "cosine"}
    )

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    client.persist()
    print("[done] Index built and saved.")


if __name__ == "__main__":
    main()