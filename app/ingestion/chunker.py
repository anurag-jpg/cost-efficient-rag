import hashlib

from app.config import settings
from app.ingestion.models import DocumentChunk, LoadedDocument


def split_into_chunks(
    document: LoadedDocument,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[DocumentChunk]:

    size = settings.chunk_size if chunk_size is None else chunk_size
    overlap = (
        settings.chunk_overlap
        if chunk_overlap is None
        else chunk_overlap
    )

    if size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= size:
        raise ValueError(
            "chunk_overlap must be non-negative and smaller than chunk_size"
        )

    text = document.content.strip()

    if not text:
        return []

    chunks = []
    step = size - overlap

    for index, start in enumerate(range(0, len(text), step)):
        content = text[start : start + size].strip()

        if not content:
            continue

        chunk_id = hashlib.sha256(
            f"{document.source}\0{content}".encode("utf-8")
        ).hexdigest()

        content_hash = hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()

        chunks.append(
            DocumentChunk(
                id=chunk_id,
                source=document.source,
                content=content,
                chunk_index=index,
                content_hash=content_hash,
            )
        )

    return chunks