from pathlib import Path

from backend.ingestion.chunker import chunk_document
from backend.ingestion.loaders import load_pdf
from backend.ingestion.models import Document, DocumentChunk


SUPPORTED_FILE_TYPES = {
    ".pdf",
    ".txt",
    ".md",
}


def load_text_file(file_path: str) -> Document:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() not in {".txt", ".md"}:
        raise ValueError("Expected a TXT or Markdown file")

    content = path.read_text(encoding="utf-8")

    return Document(
        document_id=f"file-{path.stem}",
        content=content,
        source=str(path),
        source_type=path.suffix.lower().lstrip("."),
        metadata={
            "filename": path.name,
        },
    )


def load_document(file_path: str) -> Document:
    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    if extension in {".txt", ".md"}:
        return load_text_file(file_path)

    raise ValueError(
        f"Unsupported file type: {extension or 'unknown'}"
    )


def ingest_file(
    file_path: str,
    chunk_size: int = 10000,
    chunk_overlap: int = 1000,
) -> tuple[Document, list[DocumentChunk]]:

    document = load_document(file_path)

    chunks = chunk_document(
        document,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return document, chunks
