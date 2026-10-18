from pathlib import Path

import pytest

from app.ingestion.chunker import split_into_chunks
from app.ingestion.loaders import load_document


def test_load_markdown(tmp_path: Path):
    file_path = tmp_path / "sample.md"
    file_path.write_text(
        "# Policy\nRefunds are available within 30 days.",
        encoding="utf-8",
    )

    document = load_document(file_path)

    assert document.source == "sample.md"
    assert "30 days" in document.content
    assert len(document.content_hash) == 64


def test_chunking_respects_size_and_overlap():
    from app.ingestion.models import LoadedDocument

    document = LoadedDocument(
        source="sample.md",
        content="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        content_hash="test-hash",
    )

    chunks = split_into_chunks(
        document,
        chunk_size=10,
        chunk_overlap=2,
    )

    assert chunks[0].content == "ABCDEFGHIJ"
    assert chunks[1].content.startswith("IJ")
    assert all(len(chunk.content) <= 10 for chunk in chunks)


def test_chunk_ids_are_deterministic():
    from app.ingestion.models import LoadedDocument

    document = LoadedDocument(
        source="sample.md",
        content="A short document for testing.",
        content_hash="test-hash",
    )

    first = split_into_chunks(document, 10, 2)
    second = split_into_chunks(document, 10, 2)

    assert [chunk.id for chunk in first] == [
        chunk.id for chunk in second
    ]


def test_invalid_overlap_raises_error():
    from app.ingestion.models import LoadedDocument

    document = LoadedDocument(
        source="sample.md",
        content="Some test content.",
        content_hash="test-hash",
    )

    with pytest.raises(ValueError):
        split_into_chunks(document, chunk_size=10, chunk_overlap=10)


def test_unsupported_file_type(tmp_path: Path):
    file_path = tmp_path / "sample.exe"
    file_path.write_text("not a document", encoding="utf-8")

    with pytest.raises(ValueError):
        load_document(file_path)