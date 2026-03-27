import os
from app.ingest import ingest_pdf


def test_ingest_pdf_returns_list():
    pdf_path = "data/sample.pdf"

    if not os.path.exists(pdf_path):
        return

    chunks = ingest_pdf(pdf_path)

    assert isinstance(chunks, list)
    if chunks:
        assert "text" in chunks[0]
        assert "metadata" in chunks[0]