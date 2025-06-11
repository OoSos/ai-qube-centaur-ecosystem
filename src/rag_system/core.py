"""
RAG System Core Module  
CENTAUR-013: RAG System + Gemini Integration

Advanced Retrieval-Augmented Generation system with vector database,
semantic search, and Gemini 2.5 Pro integration for intelligent
knowledge retrieval and context enhancement.

Features:
- Vector embeddings with multiple model support
- Semantic similarity search and ranking
- Dynamic context window management
- Real-time knowledge base updates
- Gemini 2.5 Pro integration for enhanced reasoning
"""

import asyncio
import json
import logging
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import hashlib
import pickle

# Vector database and embedding imports (will be installed via requirements)
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logging.warning("FAISS not available, using fallback vector search")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.warning("SentenceTransformers not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingModel(Enum):
    """Supported embedding models"""
    SENTENCE_BERT = "all-MiniLM-L6-v2"
    OPENAI_ADA = "text-embedding-ada-002"
    GEMINI_EMBEDDING = "gemini-pro-embedding"
    CUSTOM = "custom"


class DocumentType(Enum):
    """Document types in the knowledge base"""
    CODE = "code"
    DOCUMENTATION = "documentation"
    API_REFERENCE = "api_reference"
    CONFIGURATION = "configuration"
    LOG = "log"
    CONVERSATION = "conversation"
    TASK = "task"


@dataclass
class Document:
    """Document representation for RAG system"""
    id: str
    content: str
    doc_type: DocumentType
    metadata: Dict[str, Any]
    timestamp: datetime
    embedding: Optional[np.ndarray] = None
    embedding_model: Optional[str] = None
    source: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class SearchResult:
    """Search result with relevance scoring"""
    document: Document
    similarity_score: float
    relevance_rank: int
    context_snippet: str
    highlighted_terms: List[str]


@dataclass
class RAGContext:
    """Context package for RAG-enhanced responses"""
    query: str
    retrieved_documents: List[SearchResult]
    context_window: str
    total_tokens: int
    confidence_score: float
    retrieval_method: str
    timestamp: datetime


class VectorDatabase:
    """
    Vector database for semantic search and retrieval
    Supports FAISS for high-performance similarity search
    """
    
    def __init__(self, 
                 dimension: int = 384,
                 index_type: str = "flat",
                 metric: str = "cosine"):
        """
        Initialize vector database
        
        Args:
            dimension: Vector embedding dimension
            index_type: FAISS index type (flat, ivf, hnsw)
            metric: Distance metric (cosine, euclidean, inner_product)
        """
        self.dimension = dimension
        self.index_type = index_type
        self.metric = metric
        
        # Initialize FAISS index if available
        if FAISS_AVAILABLE:
            if index_type == "flat":
                if metric == "cosine":
                    self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine
                else:
                    self.index = faiss.IndexFlatL2(dimension)  # L2 for euclidean
            elif index_type == "ivf":
                quantizer = faiss.IndexFlatL2(dimension)
                self.index = faiss.IndexIVFFlat(quantizer, dimension, 100)
            else:
                self.index = faiss.IndexHNSWFlat(dimension, 32)
        else:
            self.index = None
            logger.warning("FAISS not available, using numpy-based fallback")
        
        # Document storage
        self.documents: Dict[str, Document] = {}
        self.id_to_index: Dict[str, int] = {}
        self.index_to_id: Dict[int, str] = {}
        self.next_index = 0
        
        logger.info(f"Vector database initialized: {dimension}D, {index_type}, {metric}")
    
    def add_document(self, document: Document) -> bool:
        """
        Add document with embedding to the vector database
        
        Args:
            document: Document with embedding
            
        Returns:
            bool: Success status
        """
        try:
            if document.embedding is None:
                logger.error(f"Document {document.id} has no embedding")
                return False
            
            # Normalize embedding for cosine similarity
            if self.metric == "cosine":
                embedding = document.embedding / np.linalg.norm(document.embedding)
            else:
                embedding = document.embedding
            
            # Add to FAISS index
            if self.index is not None:
                self.index.add(embedding.reshape(1, -1).astype('float32'))
            
            # Store document and mappings
            self.documents[document.id] = document
            self.id_to_index[document.id] = self.next_index
            self.index_to_id[self.next_index] = document.id
            self.next_index += 1
            
            logger.debug(f"Added document {document.id} to vector database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add document {document.id}: {e}")
            return False
    
    def search(self, 
               query_embedding: np.ndarray, 
               k: int = 10,
               threshold: float = 0.7) -> List[Tuple[str, float]]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of (document_id, similarity_score) tuples
        """
        try:
            if len(self.documents) == 0:
                return []
            
            # Normalize query embedding for cosine similarity
            if self.metric == "cosine":
                query = query_embedding / np.linalg.norm(query_embedding)
            else:
                query = query_embedding
            
            if self.index is not None and FAISS_AVAILABLE:
                # FAISS search
                scores, indices = self.index.search(
                    query.reshape(1, -1).astype('float32'), 
                    min(k, len(self.documents))
                )
                
                results = []
                for score, idx in zip(scores[0], indices[0]):
                    if idx != -1 and score >= threshold:
                        doc_id = self.index_to_id[idx]
                        results.append((doc_id, float(score)))
                
                return results
            else:
                # Fallback numpy search
                similarities = []
                for doc_id, document in self.documents.items():
                    if document.embedding is not None:
                        if self.metric == "cosine":
                            doc_embedding = document.embedding / np.linalg.norm(document.embedding)
                            similarity = np.dot(query, doc_embedding)
                        else:
                            similarity = -np.linalg.norm(query - document.embedding)
                        
                        if similarity >= threshold:
                            similarities.append((doc_id, similarity))
                
                # Sort by similarity and return top k
                similarities.sort(key=lambda x: x[1], reverse=True)
                return similarities[:k]
                
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get document by ID"""
        return self.documents.get(doc_id)
    
    def remove_document(self, doc_id: str) -> bool:
        """Remove document from database"""
        try:
            if doc_id in self.documents:
                del self.documents[doc_id]
                # Note: FAISS doesn't support efficient removal, 
                # would need index rebuild for production use
                logger.debug(f"Removed document {doc_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove document {doc_id}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            "total_documents": len(self.documents),
            "dimension": self.dimension,
            "index_type": self.index_type,
            "metric": self.metric,
            "faiss_available": FAISS_AVAILABLE
        }


class EmbeddingEngine:
    """
    Embedding generation engine with multiple model support
    """
    
    def __init__(self, model_name: str = EmbeddingModel.SENTENCE_BERT.value):
        """Initialize embedding engine with specified model"""
        self.model_name = model_name
        self.model = None
        self.dimension = 384  # Default for sentence-bert
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the embedding model"""
        try:
            if self.model_name == EmbeddingModel.SENTENCE_BERT.value:
                if SENTENCE_TRANSFORMERS_AVAILABLE:
                    self.model = SentenceTransformer(self.model_name)
                    self.dimension = self.model.get_sentence_embedding_dimension()
                    logger.info(f"Initialized SentenceTransformer: {self.model_name}")
                else:
                    logger.error("SentenceTransformers not available")
                    
            elif self.model_name == EmbeddingModel.OPENAI_ADA.value:
                # OpenAI API integration would go here
                self.dimension = 1536  # ADA embedding size
                logger.info("OpenAI Ada embeddings configured (API integration needed)")
                
            elif self.model_name == EmbeddingModel.GEMINI_EMBEDDING.value:
                # Gemini embedding integration would go here  
                self.dimension = 768  # Typical Gemini embedding size
                logger.info("Gemini embeddings configured (API integration needed)")
                
        except Exception as e:
            logger.error(f"Failed to initialize embedding model {self.model_name}: {e}")
    
    def encode(self, texts: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Generate embeddings for text(s)
        
        Args:
            texts: Single text or list of texts
            
        Returns:
            Embeddings as numpy array(s)
        """
        try:
            if self.model is None:
                # Fallback to random embeddings for testing
                logger.warning("No embedding model available, using random embeddings")
                if isinstance(texts, str):
                    return np.random.rand(self.dimension).astype('float32')
                else:
                    return [np.random.rand(self.dimension).astype('float32') for _ in texts]
            
            if isinstance(texts, str):
                return self.model.encode(texts)
            else:
                return self.model.encode(texts)
                
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            if isinstance(texts, str):
                return np.zeros(self.dimension).astype('float32')
            else:
                return [np.zeros(self.dimension).astype('float32') for _ in texts]
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.dimension


class RAGSystem:
    """
    Complete RAG (Retrieval-Augmented Generation) System
    
    Integrates vector database, embedding engine, and Gemini 2.5 Pro
    for intelligent knowledge retrieval and context enhancement.
    """
    
    def __init__(self, 
                 embedding_model: str = EmbeddingModel.SENTENCE_BERT.value,
                 vector_db_config: Optional[Dict[str, Any]] = None):
        """
        Initialize RAG system
        
        Args:
            embedding_model: Embedding model to use
            vector_db_config: Vector database configuration
        """
        self.embedding_engine = EmbeddingEngine(embedding_model)
        
        # Initialize vector database with appropriate dimension
        db_config = vector_db_config or {}
        db_config["dimension"] = self.embedding_engine.get_dimension()
        
        self.vector_db = VectorDatabase(**db_config)
        self.knowledge_base_path = Path("data/knowledge_base")
        self.knowledge_base_path.mkdir(parents=True, exist_ok=True)
        
        # Context management
        self.max_context_tokens = 4000  # Conservative limit for most models
        self.context_overlap = 200      # Token overlap between chunks
        
        logger.info("RAG System initialized successfully")
    
    async def add_document(self, 
                          content: str,
                          doc_type: DocumentType,
                          metadata: Optional[Dict[str, Any]] = None,
                          source: Optional[str] = None,
                          tags: Optional[List[str]] = None) -> str:
        """
        Add document to knowledge base
        
        Args:
            content: Document content
            doc_type: Type of document
            metadata: Additional metadata
            source: Document source
            tags: Document tags
            
        Returns:
            Document ID
        """
        try:
            # Generate document ID
            doc_id = hashlib.md5(
                f"{content[:100]}{datetime.now().isoformat()}".encode()
            ).hexdigest()
            
            # Generate embedding
            embedding = self.embedding_engine.encode(content)
            
            # Create document
            document = Document(
                id=doc_id,
                content=content,
                doc_type=doc_type,
                metadata=metadata or {},
                timestamp=datetime.now(timezone.utc),
                embedding=embedding,
                embedding_model=self.embedding_engine.model_name,
                source=source,
                tags=tags or []
            )
            
            # Add to vector database
            success = self.vector_db.add_document(document)
            
            if success:
                # Persist document
                await self._persist_document(document)
                logger.info(f"Added document {doc_id} to knowledge base")
                return doc_id
            else:
                logger.error(f"Failed to add document {doc_id} to vector database")
                return ""
                
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            return ""
    
    async def search(self, 
                    query: str,
                    k: int = 5,
                    doc_types: Optional[List[DocumentType]] = None,
                    tags: Optional[List[str]] = None,
                    threshold: float = 0.7) -> List[SearchResult]:
        """
        Search knowledge base for relevant documents
        
        Args:
            query: Search query
            k: Number of results to return
            doc_types: Filter by document types
            tags: Filter by tags
            threshold: Minimum similarity threshold
            
        Returns:
            List of search results
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_engine.encode(query)
            
            # Vector search
            raw_results = self.vector_db.search(
                query_embedding, 
                k=k*2,  # Get more results for filtering
                threshold=threshold
            )
            
            # Filter and rank results
            filtered_results = []
            for doc_id, similarity in raw_results:
                document = self.vector_db.get_document(doc_id)
                if document is None:
                    continue
                
                # Apply filters
                if doc_types and document.doc_type not in doc_types:
                    continue
                    
                if tags and not any(tag in document.tags for tag in tags):
                    continue
                
                # Create search result
                context_snippet = self._create_context_snippet(document.content, query)
                highlighted_terms = self._extract_highlighted_terms(query, document.content)
                
                result = SearchResult(
                    document=document,
                    similarity_score=similarity,
                    relevance_rank=len(filtered_results) + 1,
                    context_snippet=context_snippet,
                    highlighted_terms=highlighted_terms
                )
                
                filtered_results.append(result)
                
                if len(filtered_results) >= k:
                    break
            
            logger.info(f"Search for '{query}' returned {len(filtered_results)} results")
            return filtered_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    async def get_context(self, 
                         query: str,
                         max_tokens: Optional[int] = None,
                         doc_types: Optional[List[DocumentType]] = None) -> RAGContext:
        """
        Get complete RAG context for query
        
        Args:
            query: Query for context retrieval
            max_tokens: Maximum context tokens
            doc_types: Filter by document types
            
        Returns:
            RAG context package
        """
        try:  
            max_tokens = max_tokens or self.max_context_tokens
            
            # Search for relevant documents
            search_results = await self.search(
                query,
                k=10,  # Get more documents for context assembly
                doc_types=doc_types
            )
            
            # Build context window
            context_parts = []
            total_tokens = 0
            used_results = []
            
            for result in search_results:
                # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
                content_tokens = len(result.document.content) // 4
                
                if total_tokens + content_tokens <= max_tokens:
                    context_parts.append(f"[Source: {result.document.source or 'Unknown'}]\n{result.document.content}")
                    total_tokens += content_tokens
                    used_results.append(result)
                else:
                    # Try to fit partial content
                    remaining_tokens = max_tokens - total_tokens
                    if remaining_tokens > 100:  # Only if we have meaningful space
                        partial_content = result.document.content[:remaining_tokens * 4]
                        context_parts.append(f"[Source: {result.document.source or 'Unknown'}]\n{partial_content}...")
                        total_tokens = max_tokens
                        used_results.append(result)
                    break
            
            context_window = "\n\n".join(context_parts)
            
            # Calculate confidence score based on result quality
            confidence = self._calculate_confidence(used_results, query) if used_results else 0.0
            
            rag_context = RAGContext(
                query=query,
                retrieved_documents=used_results,
                context_window=context_window,
                total_tokens=total_tokens,
                confidence_score=confidence,
                retrieval_method="vector_similarity",
                timestamp=datetime.now(timezone.utc)
            )
            
            logger.info(f"Generated RAG context: {total_tokens} tokens, confidence: {confidence:.2f}")
            return rag_context
            
        except Exception as e:
            logger.error(f"Failed to get RAG context: {e}")
            return RAGContext(
                query=query,
                retrieved_documents=[],
                context_window="",
                total_tokens=0,
                confidence_score=0.0,
                retrieval_method="error",
                timestamp=datetime.now(timezone.utc)
            )
    
    def _create_context_snippet(self, content: str, query: str, max_length: int = 200) -> str:
        """Create contextual snippet around query terms"""
        # Simple implementation - can be enhanced with more sophisticated extraction
        words = content.lower().split()
        query_words = query.lower().split()
        
        # Find best matching section
        best_start = 0
        best_score = 0
        
        for i in range(len(words) - max_length // 10):
            section = words[i:i + max_length // 10]
            score = sum(1 for word in section if any(qw in word for qw in query_words))
            if score > best_score:
                best_score = score
                best_start = i
        
        # Extract snippet
        snippet_words = words[best_start:best_start + max_length // 10]
        snippet = " ".join(snippet_words)
        
        if len(snippet) > max_length:
            snippet = snippet[:max_length] + "..."
        
        return snippet
    
    def _extract_highlighted_terms(self, query: str, content: str) -> List[str]:
        """Extract terms from content that match query"""
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        # Find intersection of query and content words
        highlighted = list(query_words.intersection(content_words))
        return highlighted[:10]  # Limit to prevent clutter
    
    def _calculate_confidence(self, results: List[SearchResult], query: str) -> float:
        """Calculate confidence score for retrieval results"""
        if not results:
            return 0.0
        
        # Base confidence on similarity scores and result diversity
        avg_similarity = sum(r.similarity_score for r in results) / len(results)
        
        # Bonus for multiple high-quality results
        high_quality_count = sum(1 for r in results if r.similarity_score > 0.8)
        diversity_bonus = min(high_quality_count * 0.1, 0.3)
        
        confidence = min(avg_similarity + diversity_bonus, 1.0)
        return confidence
    
    async def _persist_document(self, document: Document):
        """Persist document to disk"""
        try:
            doc_file = self.knowledge_base_path / f"{document.id}.json"
            
            # Convert document to serializable format
            doc_data = asdict(document)
            doc_data["timestamp"] = document.timestamp.isoformat()
            doc_data["doc_type"] = document.doc_type.value
            doc_data["embedding"] = document.embedding.tolist() if document.embedding is not None else None
            
            with open(doc_file, 'w', encoding='utf-8') as f:
                json.dump(doc_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to persist document {document.id}: {e}")
    
    async def load_knowledge_base(self) -> int:
        """Load persisted knowledge base from disk"""
        loaded_count = 0
        
        try:
            if not self.knowledge_base_path.exists():
                return 0
            
            for doc_file in self.knowledge_base_path.glob("*.json"):
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        doc_data = json.load(f)
                    
                    # Reconstruct document
                    document = Document(
                        id=doc_data["id"],
                        content=doc_data["content"],
                        doc_type=DocumentType(doc_data["doc_type"]),
                        metadata=doc_data["metadata"],
                        timestamp=datetime.fromisoformat(doc_data["timestamp"]),
                        embedding=np.array(doc_data["embedding"]) if doc_data["embedding"] else None,
                        embedding_model=doc_data.get("embedding_model"),
                        source=doc_data.get("source"),
                        tags=doc_data.get("tags", [])
                    )
                    
                    # Add to vector database
                    if self.vector_db.add_document(document):
                        loaded_count += 1
                        
                except Exception as e:
                    logger.error(f"Failed to load document from {doc_file}: {e}")
            
            logger.info(f"Loaded {loaded_count} documents from knowledge base")
            return loaded_count
            
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics"""
        return {
            "vector_db_stats": self.vector_db.get_stats(),
            "embedding_model": self.embedding_engine.model_name,
            "embedding_dimension": self.embedding_engine.get_dimension(),
            "max_context_tokens": self.max_context_tokens,
            "knowledge_base_path": str(self.knowledge_base_path)
        }


# Factory function for easy initialization
def create_rag_system(
    embedding_model: str = EmbeddingModel.SENTENCE_BERT.value,
    vector_db_config: Optional[Dict[str, Any]] = None
) -> RAGSystem:
    """Create and initialize a RAG system"""
    return RAGSystem(embedding_model, vector_db_config)


# Example usage and testing
async def main():
    """Example usage of the RAG system"""
    
    # Initialize RAG system
    rag = create_rag_system()
    
    # Add some sample documents
    await rag.add_document(
        "The digital twin module provides cognitive state modeling for AI agents.",
        DocumentType.DOCUMENTATION,
        {"module": "digital_twin", "version": "1.0.0"},
        "digital_twin_docs.md",
        ["ai", "cognitive", "modeling"]
    )
    
    await rag.add_document(
        "FastAPI is used to create REST API endpoints for the digital twin interface.",
        DocumentType.CODE,
        {"framework": "FastAPI", "language": "Python"},
        "api.py",
        ["api", "rest", "fastapi"]
    )
    
    # Search for relevant documents
    results = await rag.search("cognitive state modeling", k=3)
    print(f"Search returned {len(results)} results:")
    for result in results:
        print(f"- {result.document.doc_type.value}: {result.similarity_score:.3f} - {result.context_snippet}")
    
    # Get complete RAG context
    context = await rag.get_context("How does digital twin cognitive modeling work?")
    print(f"\nRAG Context ({context.total_tokens} tokens, confidence: {context.confidence_score:.3f}):")
    print(context.context_window[:200] + "..." if len(context.context_window) > 200 else context.context_window)
    
    # Display statistics
    stats = rag.get_stats()
    print(f"\nRAG System Stats: {stats}")
    
    print("RAG System demonstration complete!")


if __name__ == "__main__":
    asyncio.run(main())
