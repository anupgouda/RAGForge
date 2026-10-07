from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IngestionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Document:
    document_id: str
    content: str
    source: str
    source_type: str
    version: int = 1
    status: IngestionStatus = IngestionStatus.PENDING
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentChunk:
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
    metadata: dict[str, Any] = field(default_factory=dict)
