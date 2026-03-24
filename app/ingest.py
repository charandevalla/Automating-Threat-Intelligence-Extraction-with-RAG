from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from app.extractors import extract_iocs


def ingest_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)

    processed_chunks = []

    for chunk in chunks:
        text = chunk.page_content
        metadata = chunk.metadata or {}

        iocs = extract_iocs(text)

        processed_chunks.append({
            "text": text,
            "metadata": {
                **metadata,
                **iocs
            }
        })

    return processed_chunks