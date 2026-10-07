from backend.ingestion.chunker import chunk_document
from backend.ingestion.models import Document


def test_document_chunking():
    document = Document(
        document_id="doc-001",
        content="A " * 1000,
        source="test.txt",
        source_type="txt",
    )

    chunks = chunk_document(
        document,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert len(chunks) > 1

    assert all(
        chunk.document_id == "doc-001"
        for chunk in chunks
    )

    assert all(
        chunk.content
        for chunk in chunks
    )


def test_invalid_chunk_configuration():
    document = Document(
        document_id="doc-002",
        content="test document",
        source="test.txt",
        source_type="txt",
    )

    try:
        chunk_document(
            document,
            chunk_size=100,
            chunk_overlap=100,
        )
        assert False, "Expected ValueError"

    except ValueError:
        assert True


def test_document_defaults():
    from backend.ingestion.models import IngestionStatus

    document = Document(
        document_id="doc-003",
        content="Test document",
        source="test.txt",
        source_type="txt",
    )

    assert document.version == 1
    assert document.status == IngestionStatus.PENDING
    assert document.error is None


def test_document_failed_state():
    from backend.ingestion.models import IngestionStatus

    document = Document(
        document_id="doc-004",
        content="",
        source="broken.pdf",
        source_type="pdf",
        status=IngestionStatus.FAILED,
        error="Unable to extract text",
    )

    assert document.status == IngestionStatus.FAILED
    assert document.error == "Unable to extract text"
