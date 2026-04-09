import os
import pytest
from assistant.rag import RAGPipeline


def test_index_exists():
    assert os.path.exists("data/index"), "Index directory missing"


def test_pipeline_loads():
    pipeline = RAGPipeline()
    assert pipeline.collection is not None
    assert pipeline.embedder is not None


def test_retrieval_returns_results():
    pipeline = RAGPipeline()
    docs, meta = pipeline.retrieve("What is a segment in Smash Hit?")
    assert len(docs) > 0
    assert isinstance(docs[0], str)


def test_prompt_building():
    pipeline = RAGPipeline()
    prompt = pipeline.build_prompt("Test question", ["Example context"])
    assert "Example context" in prompt
    assert "Test question" in prompt


@pytest.mark.skip(reason="LLM call requires local model runtime")
def test_llm_call():
    pipeline = RAGPipeline()
    answer, docs, meta = pipeline.answer("What is a room in Smash Hit?")
    assert isinstance(answer, str)
    assert len(answer) > 0