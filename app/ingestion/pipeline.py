from pathlib import Path

from app.ingestion.chunker import split_into_chunks
from app.ingestion.loaders import load_document
from app.ingestion.models import DocumentChunk


def ingest_file(file_path: str | Path) -> list[DocumentChunk]:
    document = load_document(file_path)
    return split_into_chunks(document)