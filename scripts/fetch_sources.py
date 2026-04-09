import os
import yaml
import requests
from git import Repo

CONFIG_PATH = "config/data_sources.yaml"


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def clone_repo(url: str, dest: str):
    if os.path.exists(dest):
        print(f"[skip] Repo already exists: {dest}")
        return
    print(f"[clone] {url} → {dest}")
    Repo.clone_from(url, dest)


def download_wiki_page(base_url: str, page: str, dest: str):
    url = f"{base_url}/{page}"
    print(f"[fetch] {url}")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"[error] Failed to fetch {page} ({response.status_code})")
        return

    with open(os.path.join(dest, page), "w", encoding="utf-8") as f:
        f.write(response.text)


def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    raw_path = config["output_paths"]["raw"]
    github_path = os.path.join(raw_path, "github")
    wiki_path = os.path.join(raw_path, "wiki")

    ensure_dir(raw_path)
    ensure_dir(github_path)
    ensure_dir(wiki_path)

    # --- GitHub repos ---
    for repo in config.get("github_repos", []):
        name = repo["name"].replace(" ", "-").lower()
        dest = os.path.join(github_path, name)
        clone_repo(repo["url"], dest)

    # --- Wiki pages ---
    base_url = config["wiki_pages"]["base_url"]
    for page in config["wiki_pages"]["pages"]:
        download_wiki_page(base_url, page, wiki_path)

    print("\n[done] All sources fetched.")


if __name__ == "__main__":
    main()
