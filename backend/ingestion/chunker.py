from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.ingestion.models import Document, DocumentChunk


def chunk_document(
    document: Document,
    chunk_size: int = 10000,
    chunk_overlap: int = 1000,
) -> list[DocumentChunk]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_text(document.content)

    return [
        DocumentChunk(
            chunk_id=str(uuid4()),
            document_id=document.document_id,
            content=content,
            chunk_index=index,
            metadata={
                **document.metadata,
                "source": document.source,
                "source_type": document.source_type,
            },
        )
        for index, content in enumerate(chunks)
    ]
