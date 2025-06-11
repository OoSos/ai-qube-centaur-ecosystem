"""
RAG System Module
CENTAUR-013: RAG System + Gemini Integration

This module provides advanced Retrieval-Augmented Generation capabilities
with vector database search and Gemini 2.5 Pro integration.

Key Components:
- Core: Vector database and embedding engine
- Gemini Integration: Enhanced reasoning with Gemini 2.5 Pro
- API: REST API interface for RAG system interaction

Usage:
    from rag_system import create_rag_system, create_gemini_rag_system
    
    # Initialize RAG system
    rag = create_rag_system()
    
    # Add documents
    await rag.add_document("content", DocumentType.DOCUMENTATION)
    
    # Search with Gemini enhancement
    gemini_rag = create_gemini_rag_system(rag, api_key="your-key")
    result = await gemini_rag.enhanced_query("question", ResponseMode.REASONING)
"""

from .core import (
    RAGSystem,
    VectorDatabase,
    EmbeddingEngine,
    Document,
    SearchResult,
    RAGContext,
    DocumentType,
    EmbeddingModel,
    create_rag_system
)

from .gemini_integration import (
    GeminiRAGIntegration,
    GeminiResponse,
    EnhancedRAGResult,
    GeminiModel,
    ResponseMode,
    create_gemini_rag_system
)

__version__ = "1.0.0"
__author__ = "AI Qube Centaur Ecosystem"

__all__ = [
    # Core RAG components
    "RAGSystem",
    "VectorDatabase", 
    "EmbeddingEngine",
    "Document",
    "SearchResult",
    "RAGContext",
    "DocumentType",
    "EmbeddingModel",
    "create_rag_system",
    
    # Gemini integration
    "GeminiRAGIntegration",
    "GeminiResponse",
    "EnhancedRAGResult", 
    "GeminiModel",
    "ResponseMode",
    "create_gemini_rag_system"
]

# Module level convenience functions
async def quick_search(query: str, 
                      documents: list = None,
                      embedding_model: str = EmbeddingModel.SENTENCE_BERT.value) -> list:
    """Quick search without persistent storage"""
    rag = create_rag_system(embedding_model)
    
    if documents:
        for doc_content in documents:
            await rag.add_document(doc_content, DocumentType.DOCUMENTATION)
    
    results = await rag.search(query)
    return results

async def enhanced_search(query: str,
                         documents: list = None, 
                         gemini_api_key: str = None,
                         response_mode: ResponseMode = ResponseMode.REASONING):
    """Enhanced search with Gemini reasoning"""
    rag = create_rag_system()
    
    if documents:
        for doc_content in documents:
            await rag.add_document(doc_content, DocumentType.DOCUMENTATION)
    
    gemini_rag = create_gemini_rag_system(rag, gemini_api_key)
    result = await gemini_rag.enhanced_query(query, response_mode)
    return result
