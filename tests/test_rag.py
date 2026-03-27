import pytest
from app.rag import ThreatIntelRAG


@pytest.mark.skip(reason="Requires running Qdrant and indexed documents")
def test_rag_response_structure():
    rag = ThreatIntelRAG()
    answer, context_chunks, sources, metadata_summary = rag.ask("Summarize the main points", top_k=3)

    assert isinstance(answer, str)
    assert isinstance(context_chunks, list)
    assert isinstance(sources, list)
    assert isinstance(metadata_summary, dict)