from pathlib import Path

import pytest

from backend.ingestion.service import (
    ingest_file,
    load_document,
)


def test_load_txt(tmp_path: Path):
    file_path = tmp_path / "sample.txt"

    file_path.write_text(
        "RAGForge is an evaluation-driven RAG platform.",
        encoding="utf-8",
    )

    document = load_document(str(file_path))

    assert document.source_type == "txt"
    assert document.content.startswith("RAGForge")
    assert document.metadata["filename"] == "sample.txt"


def test_load_markdown(tmp_path: Path):
    file_path = tmp_path / "sample.md"

    file_path.write_text(
        "# RAGForge\n\nProduction RAG systems need evaluation.",
        encoding="utf-8",
    )

    document = load_document(str(file_path))

    assert document.source_type == "md"
    assert "Production RAG" in document.content


def test_unsupported_file(tmp_path: Path):
    file_path = tmp_path / "sample.csv"

    file_path.write_text(
        "name,value\nA,10",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_document(str(file_path))


def test_ingest_file(tmp_path: Path):
    file_path = tmp_path / "large.txt"

    file_path.write_text(
        "RAGForge evaluation. " * 1000,
        encoding="utf-8",
    )

    document, chunks = ingest_file(
        str(file_path),
        chunk_size=200,
        chunk_overlap=40,
    )

    assert document.source_type == "txt"
    assert len(chunks) > 1

    assert all(
        chunk.document_id == document.document_id
        for chunk in chunks
    )
