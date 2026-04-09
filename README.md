# Smash Hit Lab - Local AI Assistant 
A fully local, retrieval-augmented AI assistant designed to help creators learn and work with **Smash Hit Modding Tools, workflows, and documentation**. No cloud APIs. No external dependencies. Everything runs on your machine.

## What This Assistant Does
- Answers questions about **Smash Hit modding** including:
  - Segments, rooms, levels, and game structure
  - Mesh formats, baking, and Blender workflows
  - Tools like Shatter, Mesh-Bake, and other community utilities 
- Provides **step-by-step guidance** for common modding tasks.
- Retrieves information from:
  - Smash Hit Lab documentation
  - Smash Hit Lab Wiki pages
  - GitHub READMEs from community tools
- Runs **entirely offline** using a local LLM + local vector database
- Designed for modders, creators, and community maintainers.

## Quickstart
### 1. Install dependencies
You'll need

- Python 3.10+
- A local LLM runtime (e.g. Ollama or LM Studio)
- A supported embedding model

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Fetch documentation sources
This pulls Smash Hit Lab docs, wiki pages, and tool READMEs into ``data/raw/``.

```bash
python scripts/fetch_sources.py
```

### 3. Preprocess and chunk the data
Convert HTML/markdown -> clean text -> chunked segments.

```bash
python scripts/preprocess.py
```

### 4. Build the vector index
Embeds all chunks and stores them in ``data/index/``.

```bash
python scripts/build_index.py
```

### 5. Run the assistant
Launch the local CLI:

```bash
python -m assistant.cli
```

Example:

```text
> How do I create a custom segment in Smash Hit?
```

## How It Works
### Retrieval-Augmented Generation
This assistant uses a simple but powerful architecture:

1. **User asks a question**
2. The question is embedded and matched against the local vector index
3. Relevant documentation chunks are retrieved
4. A prompt is constructed with:
  - System instructions
  - Retrieved context
  - User question
5. A local LLM generates the final answer

This ensures:

- High accuracy
- Low privacy
- Answers grounded in real modding documentation

# Configuration
``config/model.yaml``
Defines:

- Local LLM model name
- Embedding model
- Generation parameters

``config/data_sources.yaml``
Defines:

- GitHub repos to clone
- Wiki pages to fetch
- File patterns to include/exclude

# Testing
Basic tests ensure:

- Index loads correctly
- Retrieval returns relevant chunks
- Assistant pipeline runs end-to-end

Run tests: ``pytest``

# Limitations
- Not an official tool from Mediocre or Smash Hit developers
- Answers depend on the quality or indexed documentation
- May not reflect the latest community discoveries unless updated
- Does not modify or patch game files

# License
Code is licensed under **MIT**.
Documentation remains under the licenses of their original authors.