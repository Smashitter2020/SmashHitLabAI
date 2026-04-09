import yaml
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from assistant.prompts import SYSTEM_PROMPT, RETRIEVAL_TEMPLATE
import subprocess


CONFIG_MODEL = "config/model.yaml"
INDEX_DIR = "data/index"


class RAGPipeline:
    def __init__(self):
        self.config = self._load_config()
        self.model_name = self.config["llm"]["model_name"]
        self.embed_model_name = self.config["embeddings"]["model_name"]
        self.top_k = self.config["retrieval"]["top_k"]

        print(f"[rag] Loading embedding model: {self.embed_model_name}")
        self.embedder = SentenceTransformer(self.embed_model_name)

        print("[rag] Loading vector index...")
        self.collection = self._load_index()

    def _load_config(self):
        with open(CONFIG_MODEL, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _load_index(self):
        client = chromadb.Client(
            Settings(chroma_db_impl="duckdb+parquet", persist_directory=INDEX_DIR)
        )
        return client.get_collection("smash_hit_docs")

    def embed(self, text: str):
        return self.embedder.encode([text])[0]

    def retrieve(self, query: str):
        query_emb = self.embed(query)

        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=self.top_k,
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        return documents, metadatas

    def build_prompt(self, query: str, documents: list[str]):
        context = "\n\n".join(documents)
        return SYSTEM_PROMPT + "\n" + RETRIEVAL_TEMPLATE.format(
            context=context,
            question=query
        )

    def call_llm(self, prompt: str):
        # Default: Ollama. Modify if using LM Studio or llama.cpp.
        result = subprocess.run(
            ["ollama", "run", self.model_name],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode("utf-8")

    def answer(self, query: str):
        docs, meta = self.retrieve(query)
        prompt = self.build_prompt(query, docs)
        response = self.call_llm(prompt)
        return response, docs, meta