from pathlib import Path
from uuid import uuid4

from pypdf import PdfReader

from backend.ingestion.models import Document


def load_pdf(file_path: str) -> Document:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Expected a PDF file")

    reader = PdfReader(str(path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                {
                    "page": page_number,
                    "content": text.strip(),
                }
            )

    content = "\n\n".join(
        page["content"]
        for page in pages
    )

    return Document(
        document_id=str(uuid4()),
        content=content,
        source=str(path),
        source_type="pdf",
        metadata={
            "filename": path.name,
            "page_count": len(reader.pages),
            "extracted_pages": len(pages),
            "pages": pages,
        },
    )
