"""
Test Suite for RAG System Module  
CENTAUR-013: RAG System + Gemini Integration Tests

Comprehensive test coverage for:
- Vector database functionality
- Embedding generation
- Document retrieval
- Gemini integration
"""

import pytest
import asyncio
import json
import numpy as np
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch

# Import modules to test
from src.rag_system import (
    RAGSystem,
    VectorDatabase,
    EmbeddingEngine,
    Document,
    DocumentType,
    EmbeddingModel,
    create_rag_system,
    GeminiRAGIntegration,
    ResponseMode,
    create_gemini_rag_system
)


class TestVectorDatabase:
    """Test cases for Vector Database"""
    
    @pytest.fixture
    def vector_db(self):
        """Create test vector database"""
        return VectorDatabase(dimension=384, index_type="flat", metric="cosine")
    
    def test_database_initialization(self, vector_db):
        """Test database initializes correctly"""
        assert vector_db.dimension == 384
        assert vector_db.index_type == "flat"
        assert vector_db.metric == "cosine"
        assert len(vector_db.documents) == 0
    
    def test_add_document(self, vector_db):
        """Test adding document to database"""
        # Create test document with embedding
        embedding = np.random.rand(384).astype('float32')
        document = Document(
            id="test_doc_1",
            content="Test document content",
            doc_type=DocumentType.DOCUMENTATION,
            metadata={"test": True},
            timestamp=datetime.now(timezone.utc),
            embedding=embedding
        )
        
        # Add document
        success = vector_db.add_document(document)
        assert success is True
        assert len(vector_db.documents) == 1
        assert "test_doc_1" in vector_db.documents
    
    def test_search_documents(self, vector_db):
        """Test document search functionality"""
        # Add test documents
        for i in range(3):
            embedding = np.random.rand(384).astype('float32')
            document = Document(
                id=f"doc_{i}",
                content=f"Document {i} content",
                doc_type=DocumentType.DOCUMENTATION,
                metadata={"index": i},
                timestamp=datetime.now(timezone.utc),
                embedding=embedding
            )
            vector_db.add_document(document)
        
        # Search with random query embedding
        query_embedding = np.random.rand(384).astype('float32')
        results = vector_db.search(query_embedding, k=2, threshold=0.0)
        
        # Should return results
        assert len(results) <= 2
        for doc_id, similarity in results:
            assert doc_id in vector_db.documents
            assert 0.0 <= similarity <= 1.0
    
    def test_get_stats(self, vector_db):
        """Test database statistics"""
        stats = vector_db.get_stats()
        assert "total_documents" in stats
        assert "dimension" in stats
        assert stats["dimension"] == 384


class TestEmbeddingEngine:
    """Test cases for Embedding Engine"""
    
    @pytest.fixture
    def embedding_engine(self):
        """Create test embedding engine"""
        return EmbeddingEngine(EmbeddingModel.SENTENCE_BERT.value)
    
    def test_engine_initialization(self, embedding_engine):
        """Test embedding engine initialization"""
        assert embedding_engine.model_name == EmbeddingModel.SENTENCE_BERT.value
        assert embedding_engine.dimension > 0
    
    def test_single_text_encoding(self, embedding_engine):
        """Test encoding single text"""
        text = "This is a test sentence"
        embedding = embedding_engine.encode(text)
        
        assert isinstance(embedding, np.ndarray)
        assert embedding.shape[0] == embedding_engine.dimension
        assert embedding.dtype == np.float32
    
    def test_batch_text_encoding(self, embedding_engine):
        """Test encoding multiple texts"""
        texts = [
            "First test sentence",
            "Second test sentence", 
            "Third test sentence"
        ]
        embeddings = embedding_engine.encode(texts)
        
        assert isinstance(embeddings, list)
        assert len(embeddings) == 3
        for embedding in embeddings:
            assert isinstance(embedding, np.ndarray)
            assert embedding.shape[0] == embedding_engine.dimension


class TestRAGSystem:
    """Test cases for RAG System"""
    
    @pytest.fixture
    async def rag_system(self):
        """Create test RAG system"""
        return create_rag_system()
    
    @pytest.mark.asyncio
    async def test_rag_system_initialization(self, rag_system):
        """Test RAG system initialization"""
        assert rag_system is not None
        assert rag_system.embedding_engine is not None
        assert rag_system.vector_db is not None
        
        stats = rag_system.get_stats()
        assert "vector_db_stats" in stats
        assert "embedding_model" in stats
    
    @pytest.mark.asyncio
    async def test_add_document(self, rag_system):
        """Test adding document to RAG system"""
        content = "This is test documentation for the RAG system"
        doc_id = await rag_system.add_document(
            content=content,
            doc_type=DocumentType.DOCUMENTATION,
            metadata={"test": True},
            source="test.md",
            tags=["test", "documentation"]
        )
        
        assert doc_id != ""
        assert len(doc_id) > 0
        
        # Verify document was added
        stats = rag_system.get_stats()
        assert stats["vector_db_stats"]["total_documents"] == 1
    
    @pytest.mark.asyncio
    async def test_search_documents(self, rag_system):
        """Test document search"""
        # Add test documents
        await rag_system.add_document(
            "Digital twin cognitive modeling for AI agents",
            DocumentType.DOCUMENTATION,
            tags=["ai", "cognitive"]
        )
        
        await rag_system.add_document(
            "FastAPI REST API implementation guide",
            DocumentType.CODE,
            tags=["api", "fastapi"]
        )
        
        # Search for relevant documents
        results = await rag_system.search("cognitive modeling", k=2)
        
        assert len(results) > 0
        assert results[0].similarity_score > 0.0
        assert "cognitive" in results[0].document.content.lower()
    
    @pytest.mark.asyncio
    async def test_get_context(self, rag_system):
        """Test getting RAG context"""
        # Add sample documents
        await rag_system.add_document(
            "Machine learning models require training data",
            DocumentType.DOCUMENTATION
        )
        
        await rag_system.add_document(
            "Vector databases store high-dimensional embeddings",
            DocumentType.DOCUMENTATION
        )
        
        # Get context for query
        context = await rag_system.get_context("machine learning vectors")
        
        assert context.query == "machine learning vectors"
        assert context.total_tokens >= 0
        assert context.confidence_score >= 0.0
        assert isinstance(context.retrieved_documents, list)
    
    @pytest.mark.asyncio
    async def test_document_filtering(self, rag_system):
        """Test document filtering by type and tags"""
        # Add documents of different types
        await rag_system.add_document(
            "Documentation about APIs",
            DocumentType.DOCUMENTATION,
            tags=["api", "docs"]
        )
        
        await rag_system.add_document(
            "def api_function(): pass",
            DocumentType.CODE,
            tags=["api", "code"]
        )
        
        # Search with doc type filter
        doc_results = await rag_system.search(
            "API implementation",
            doc_types=[DocumentType.DOCUMENTATION]
        )
        
        code_results = await rag_system.search(
            "API implementation", 
            doc_types=[DocumentType.CODE]
        )
        
        # Should have different results
        assert len(doc_results) > 0
        assert len(code_results) > 0
        assert doc_results[0].document.doc_type == DocumentType.DOCUMENTATION
        assert code_results[0].document.doc_type == DocumentType.CODE


class TestGeminiRAGIntegration:
    """Test cases for Gemini RAG Integration"""
    
    @pytest.fixture
    async def gemini_rag(self):
        """Create test Gemini RAG integration"""
        rag_system = create_rag_system()
        # Initialize without API key for testing
        return create_gemini_rag_system(rag_system, gemini_api_key=None)
    
    @pytest.mark.asyncio
    async def test_gemini_rag_initialization(self, gemini_rag):
        """Test Gemini RAG integration initialization"""
        assert gemini_rag is not None
        assert gemini_rag.rag_system is not None
        assert gemini_rag.model_name is not None
        
        stats = gemini_rag.get_stats()
        assert "rag_system" in stats
        assert "gemini_model" in stats
        assert "response_modes" in stats
    
    @pytest.mark.asyncio
    async def test_enhanced_query_fallback(self, gemini_rag):
        """Test enhanced query with fallback (no API key)"""
        # Add test document
        await gemini_rag.rag_system.add_document(
            "Digital twins model cognitive states of AI agents",
            DocumentType.DOCUMENTATION
        )
        
        # Run enhanced query (should use fallback)
        result = await gemini_rag.enhanced_query(
            "What are digital twins?",
            ResponseMode.REASONING
        )
        
        assert result is not None
        assert result.query == "What are digital twins?"
        assert result.enhanced_answer != ""
        assert result.confidence_score >= 0.0
        assert isinstance(result.reasoning_chain, list)
    
    @pytest.mark.asyncio
    async def test_different_response_modes(self, gemini_rag):
        """Test different response modes"""
        # Add test document
        await gemini_rag.rag_system.add_document(
            "RAG systems combine retrieval with generation",
            DocumentType.DOCUMENTATION
        )
        
        query = "How do RAG systems work?"
        
        # Test different modes
        modes = [ResponseMode.DIRECT, ResponseMode.REASONING, ResponseMode.SYNTHESIS]
        
        for mode in modes:
            result = await gemini_rag.enhanced_query(query, mode)
            assert result is not None
            assert result.enhanced_answer != ""
            # Different modes should potentially give different responses
    
    @pytest.mark.asyncio 
    async def test_batch_processing(self, gemini_rag):
        """Test batch query processing"""
        # Add test documents
        await gemini_rag.rag_system.add_document(
            "AI agents can coordinate tasks",
            DocumentType.DOCUMENTATION
        )
        
        queries = [
            "What are AI agents?",
            "How do agents coordinate?",
            "What is task management?"
        ]
        
        results = await gemini_rag.batch_process_queries(queries, ResponseMode.DIRECT)
        
        assert len(results) == len(queries)
        for i, result in enumerate(results):
            assert result.query == queries[i]
            assert result.enhanced_answer != ""


class TestIntegrationScenarios:
    """Integration test scenarios"""
    
    @pytest.mark.asyncio
    async def test_full_rag_pipeline(self):
        """Test complete RAG pipeline"""
        # Initialize systems
        rag = create_rag_system()
        gemini_rag = create_gemini_rag_system(rag)
        
        # Add diverse documents
        documents = [
            ("Digital twin technology models real-world systems", DocumentType.DOCUMENTATION),
            ("Vector databases enable semantic search", DocumentType.DOCUMENTATION),
            ("class DigitalTwin: def __init__(self): pass", DocumentType.CODE),
            ("API endpoints for digital twin management", DocumentType.API_REFERENCE)
        ]
        
        for content, doc_type in documents:
            doc_id = await rag.add_document(content, doc_type)
            assert doc_id != ""
        
        # Test semantic search
        search_results = await rag.search("digital twin API", k=3)
        assert len(search_results) > 0
        
        # Test context generation
        context = await rag.get_context("digital twin implementation")
        assert context.total_tokens > 0
        assert len(context.retrieved_documents) > 0
        
        # Test enhanced query
        enhanced_result = await gemini_rag.enhanced_query(
            "How to implement digital twin APIs?",
            ResponseMode.SYNTHESIS
        )
        
        assert enhanced_result.confidence_score > 0.0
        assert len(enhanced_result.source_citations) > 0
    
    @pytest.mark.asyncio
    async def test_knowledge_base_persistence(self):
        """Test knowledge base persistence"""
        rag = create_rag_system()
        
        # Add documents
        doc_ids = []
        for i in range(3):
            doc_id = await rag.add_document(
                f"Test document {i} content",
                DocumentType.DOCUMENTATION,
                metadata={"index": i}
            )
            doc_ids.append(doc_id)
        
        # Export state
        stats_before = rag.get_stats()
        
        # Simulate reload (would load from persistence)
        # In a real scenario, this would test file-based persistence
        loaded_count = await rag.load_knowledge_base()
        
        # Verify system state
        stats_after = rag.get_stats()
        assert stats_after["vector_db_stats"]["total_documents"] >= 0


class TestPerformance:
    """Performance test cases"""
    
    @pytest.mark.asyncio
    async def test_bulk_document_addition(self):
        """Test performance with many documents"""
        rag = create_rag_system()
        
        import time
        start_time = time.time()
        
        # Add multiple documents
        for i in range(50):
            await rag.add_document(
                f"Document {i} with various content and keywords",
                DocumentType.DOCUMENTATION,
                metadata={"index": i}
            )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete within reasonable time
        assert duration < 30.0  # 30 seconds for 50 documents
        
        # Verify all documents added
        stats = rag.get_stats()
        assert stats["vector_db_stats"]["total_documents"] == 50
    
    @pytest.mark.asyncio
    async def test_search_performance(self):
        """Test search performance with many documents"""
        rag = create_rag_system()
        
        # Add documents
        for i in range(20):
            await rag.add_document(
                f"Document {i} about machine learning and AI systems",
                DocumentType.DOCUMENTATION
            )
        
        import time
        start_time = time.time()
        
        # Perform multiple searches
        for i in range(10):
            results = await rag.search(f"machine learning system {i}", k=5)
            assert len(results) > 0
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete searches quickly
        assert duration < 5.0  # 5 seconds for 10 searches


# Test fixtures and configuration
@pytest.fixture(scope="session") 
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment"""
    # Any global test setup here
    pass


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
