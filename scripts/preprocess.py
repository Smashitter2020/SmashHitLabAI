import os
import re
import yaml
from pathlib import Path
from typing import List

CONFIG_PATH = "config/data_sources.yaml"


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def clean_markdown(text: str) -> str:
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove markdown headers, links, images
    text = re.sub(r"!\[.*?\]`\(.*?\)`", " ", text)
    text = re.sub(r"\[([^\]]+)\]`\([^)]+\)`", r"\1", text)

    # Remove code fences
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def chunk_text(text: str, chunk_size=800, overlap=200) -> List[str]:
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap

    return chunks


def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    raw_dir = Path(config["output_paths"]["raw"])
    processed_dir = Path(config["output_paths"]["processed"])
    ensure_dir(processed_dir)

    all_chunks = []
    file_count = 0

    for root, _, files in os.walk(raw_dir):
        for file in files:
            if not file.lower().endswith((".md", ".txt")):
                continue

            file_path = os.path.join(root, file)
            text = load_text(file_path)
            cleaned = clean_markdown(text)
            chunks = chunk_text(cleaned)

            for i, chunk in enumerate(chunks):
                out_path = processed_dir / f"{file}_{i}.txt"
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(chunk)

            file_count += 1

    print(f"[done] Processed {file_count} files into chunks.")


if __name__ == "__main__":
    main()