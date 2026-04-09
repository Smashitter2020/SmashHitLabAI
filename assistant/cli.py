import yaml
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from assistant.prompts import SYSTEM_PROMPT, RETRIEVAL_TEMPLATE
import subprocess


CONFIG_MODEL = "config/model.yaml"
INDEX_DIR = "data/index"


def load_config():
    with open(CONFIG_MODEL, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_index():
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=INDEX_DIR))
    return client.get_collection("smash_hit_docs")


def embed(text, embedder):
    return embedder.encode([text])[0]


def call_llm(model_name, prompt):
    # Works with Ollama or LM Studio (modify as needed)
    result = subprocess.run(
        ["ollama", "run", model_name],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8")


def main():
    config = load_config()
    model_name = config["llm"]["model_name"]
    embed_model_name = config["embeddings"]["model_name"]

    print(f"[load] LLM: {model_name}")
    print(f"[load] Embeddings: {embed_model_name}")

    embedder = SentenceTransformer(embed_model_name)
    collection = load_index()

    print("\nSmash Hit Lab Local Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("> ").strip()
        if query.lower() in ("exit", "quit"):
            break

        query_emb = embed(query, embedder)

        results = collection.query(
            query_embeddings=[query_emb],
            n_results=5,
        )

        context = "\n\n".join(results["documents"][0])

        prompt = SYSTEM_PROMPT + "\n" + RETRIEVAL_TEMPLATE.format(
            context=context,
            question=query
        )

        answer = call_llm(model_name, prompt)
        print("\n" + answer + "\n")


if __name__ == "__main__":
    main()
