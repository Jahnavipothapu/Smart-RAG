"""Document models and data structures."""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

class DocumentType(Enum):
    """Supported document types."""
    PDF = "pdf"
    TEXT = "text"
    DOCX = "docx"
    HTML = "html"
    MARKDOWN = "markdown"

class ChunkType(Enum):
    """Types of document chunks."""
    PARAGRAPH = "paragraph"
    SECTION = "section"
    TABLE = "table"
    FIGURE_CAPTION = "figure_caption"
    HEADER = "header"
    FOOTER = "footer"

@dataclass
class DocumentMetadata:
    """Metadata for documents."""
    title: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    publication_date: Optional[datetime] = None
    source: Optional[str] = None
    doi: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    abstract: Optional[str] = None
    document_type: Optional[DocumentType] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    page_count: Optional[int] = None
    language: str = "en"
    
@dataclass
class DocumentChunk:
    """A chunk of document content with metadata."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    chunk_type: ChunkType = ChunkType.PARAGRAPH
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    start_char: int = 0
    end_char: int = 0
    embedding: Optional[List[float]] = None
    
    # Structural information
    heading_level: Optional[int] = None
    is_title: bool = False
    is_abstract: bool = False
    contains_citations: bool = False
    
    # Quality metrics
    word_count: int = 0
    sentence_count: int = 0
    
    def __post_init__(self):
        """Calculate derived fields."""
        if self.content:
            self.word_count = len(self.content.split())
            self.sentence_count = len([s for s in self.content.split('.') if s.strip()])

@dataclass
class Document:
    """Main document class."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    metadata: DocumentMetadata = field(default_factory=DocumentMetadata)
    chunks: List[DocumentChunk] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Processing status
    is_processed: bool = False
    is_embedded: bool = False
    processing_errors: List[str] = field(default_factory=list)
    
    def add_chunk(self, chunk: DocumentChunk) -> None:
        """Add a chunk to the document."""
        self.chunks.append(chunk)
        self.updated_at = datetime.now()
    
    def get_chunks_by_type(self, chunk_type: ChunkType) -> List[DocumentChunk]:
        """Get chunks of a specific type."""
        return [chunk for chunk in self.chunks if chunk.chunk_type == chunk_type]
    
    def get_summary_info(self) -> Dict[str, Any]:
        """Get summary information about the document."""
        return {
            "id": self.id,
            "title": self.metadata.title,
            "authors": self.metadata.authors,
            "chunk_count": len(self.chunks),
            "word_count": sum(chunk.word_count for chunk in self.chunks),
            "is_processed": self.is_processed,
            "is_embedded": self.is_embedded,
            "created_at": self.created_at.isoformat(),
        }

@dataclass
class QueryResult:
    """Result from a retrieval query."""
    chunk: DocumentChunk
    document_id: str
    score: float
    retrieval_method: str  # "semantic", "lexical", "hybrid"
    
@dataclass
class RAGResponse:
    """Complete response from the RAG system."""
    query: str
    answer: str
    sources: List[QueryResult]
    confidence_score: float
    processing_time: float
    reasoning_steps: List[str] = field(default_factory=list)
    
    def get_source_documents(self) -> List[str]:
        """Get unique document IDs from sources."""
        return list(set(result.document_id for result in self.sources))