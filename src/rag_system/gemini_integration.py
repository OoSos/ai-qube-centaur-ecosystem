"""
Gemini Integration Module
CENTAUR-013: RAG System + Gemini Integration

Advanced integration with Google Gemini 2.5 Pro for:
- Enhanced reasoning over retrieved context
- Dynamic query refinement
- Intelligent response synthesis
- Multi-modal understanding support
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum

# Gemini API integration (placeholder for actual implementation)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Google Generative AI not available")

from .core import RAGSystem, RAGContext, DocumentType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiModel(Enum):
    """Supported Gemini models"""
    GEMINI_PRO = "gemini-pro"
    GEMINI_PRO_VISION = "gemini-pro-vision"
    GEMINI_ULTRA = "gemini-ultra"


class ResponseMode(Enum):
    """Response generation modes"""
    DIRECT = "direct"                    # Direct answer from context
    REASONING = "reasoning"              # Step-by-step reasoning
    SYNTHESIS = "synthesis"              # Synthesized from multiple sources
    ANALYSIS = "analysis"                # Analytical breakdown
    CREATIVE = "creative"                # Creative/innovative response


@dataclass
class GeminiResponse:
    """Gemini API response wrapper"""
    content: str
    model: str
    timestamp: datetime
    usage_metadata: Dict[str, Any]
    confidence: float
    reasoning_steps: Optional[List[str]] = None
    sources_used: Optional[List[str]] = None
    response_mode: Optional[ResponseMode] = None


@dataclass
class EnhancedRAGResult:
    """RAG result enhanced with Gemini reasoning"""
    query: str
    rag_context: RAGContext
    gemini_response: GeminiResponse
    enhanced_answer: str
    confidence_score: float
    reasoning_chain: List[str]
    source_citations: List[Dict[str, str]]
    timestamp: datetime


class GeminiRAGIntegration:
    """
    Advanced RAG system with Gemini 2.5 Pro integration
    
    Combines vector-based retrieval with Gemini's reasoning capabilities
    for intelligent, context-aware responses.
    """
    
    def __init__(self, 
                 rag_system: RAGSystem,
                 gemini_api_key: Optional[str] = None,
                 model: str = GeminiModel.GEMINI_PRO.value):
        """
        Initialize Gemini-enhanced RAG system
        
        Args:
            rag_system: Initialized RAG system
            gemini_api_key: Gemini API key
            model: Gemini model to use
        """
        self.rag_system = rag_system
        self.model_name = model
        self.gemini_client = None
        
        # Initialize Gemini client
        if GEMINI_AVAILABLE and gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                self.gemini_client = genai.GenerativeModel(model)
                logger.info(f"Gemini {model} initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
        else:
            logger.warning("Gemini integration not available - using fallback")
        
        # Response templates
        self.response_templates = {
            ResponseMode.DIRECT: self._get_direct_template(),
            ResponseMode.REASONING: self._get_reasoning_template(),
            ResponseMode.SYNTHESIS: self._get_synthesis_template(),
            ResponseMode.ANALYSIS: self._get_analysis_template(),
            ResponseMode.CREATIVE: self._get_creative_template()
        }
        
        # Configuration
        self.max_context_length = 30000  # Gemini context window
        self.temperature = 0.7
        self.top_p = 0.9
        
        logger.info("Gemini RAG integration initialized")
    
    async def enhanced_query(self, 
                           query: str,
                           response_mode: ResponseMode = ResponseMode.REASONING,
                           doc_types: Optional[List[DocumentType]] = None,
                           max_sources: int = 5) -> EnhancedRAGResult:
        """
        Process query with enhanced RAG + Gemini reasoning
        
        Args:
            query: User query
            response_mode: How to generate the response
            doc_types: Filter retrieved documents by type
            max_sources: Maximum number of sources to use
            
        Returns:
            Enhanced RAG result with Gemini reasoning
        """
        try:
            # Phase 1: Retrieve relevant context using RAG
            logger.info(f"Retrieving context for query: {query}")
            rag_context = await self.rag_system.get_context(
                query=query,
                max_tokens=self.max_context_length // 2,  # Reserve space for prompt
                doc_types=doc_types
            )
            
            # Phase 2: Enhance query with Gemini reasoning
            enhanced_answer, gemini_response = await self._generate_enhanced_response(
                query=query,
                rag_context=rag_context,
                response_mode=response_mode,
                max_sources=max_sources
            )
            
            # Phase 3: Extract reasoning chain and citations
            reasoning_chain = self._extract_reasoning_chain(gemini_response.content)
            source_citations = self._extract_source_citations(rag_context, enhanced_answer)
            
            # Phase 4: Calculate confidence score
            confidence_score = self._calculate_enhanced_confidence(
                rag_context, gemini_response, reasoning_chain
            )
            
            result = EnhancedRAGResult(
                query=query,
                rag_context=rag_context,
                gemini_response=gemini_response,
                enhanced_answer=enhanced_answer,
                confidence_score=confidence_score,
                reasoning_chain=reasoning_chain,
                source_citations=source_citations,
                timestamp=datetime.now(timezone.utc)
            )
            
            logger.info(f"Enhanced query completed - confidence: {confidence_score:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"Enhanced query failed: {e}")
            # Return fallback result
            return self._create_fallback_result(query, str(e))
    
    async def _generate_enhanced_response(self,
                                        query: str,
                                        rag_context: RAGContext,
                                        response_mode: ResponseMode,
                                        max_sources: int) -> tuple[str, GeminiResponse]:
        """Generate enhanced response using Gemini"""
        try:
            # Prepare prompt with RAG context
            prompt = self._build_enhanced_prompt(
                query=query,
                rag_context=rag_context,
                response_mode=response_mode,
                max_sources=max_sources
            )
            
            if self.gemini_client:
                # Use actual Gemini API
                response = await self._call_gemini_api(prompt)
            else:
                # Fallback response
                response = self._generate_fallback_response(query, rag_context)
            
            # Extract enhanced answer from response
            enhanced_answer = self._extract_answer_from_response(response.content)
            
            return enhanced_answer, response
            
        except Exception as e:
            logger.error(f"Enhanced response generation failed: {e}")
            fallback_response = self._generate_fallback_response(query, rag_context)
            return fallback_response.content, fallback_response
    
    def _build_enhanced_prompt(self,
                             query: str,
                             rag_context: RAGContext,
                             response_mode: ResponseMode,
                             max_sources: int) -> str:
        """Build enhanced prompt for Gemini"""
        template = self.response_templates[response_mode]
        
        # Limit sources if needed
        limited_sources = rag_context.retrieved_documents[:max_sources]
        context_text = "\n\n".join([
            f"Source {i+1} ({doc.document.doc_type.value}): {doc.document.content[:1000]}"
            for i, doc in enumerate(limited_sources)
        ])
        
        prompt = template.format(
            query=query,
            context=context_text,
            num_sources=len(limited_sources),
            confidence=rag_context.confidence_score
        )
        
        return prompt
    
    async def _call_gemini_api(self, prompt: str) -> GeminiResponse:
        """Call Gemini API with prompt"""
        try:
            # Configure generation parameters
            generation_config = {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_output_tokens": 2048,
            }
            
            # Make API call
            response = await self.gemini_client.generate_content_async(
                prompt,
                generation_config=generation_config
            )
            
            # Parse response
            gemini_response = GeminiResponse(
                content=response.text,
                model=self.model_name,
                timestamp=datetime.now(timezone.utc),
                usage_metadata=getattr(response, 'usage_metadata', {}),
                confidence=0.8  # Default confidence for API responses
            )
            
            return gemini_response
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return self._generate_fallback_response("", None)
    
    def _generate_fallback_response(self, query: str, rag_context: Optional[RAGContext]) -> GeminiResponse:
        """Generate fallback response when Gemini is unavailable"""
        if rag_context and rag_context.retrieved_documents:
            # Use retrieved context to generate basic response
            content = f"Based on the available information:\n\n"
            content += f"Query: {query}\n\n"
            
            for i, result in enumerate(rag_context.retrieved_documents[:3]):
                content += f"Source {i+1}: {result.context_snippet}\n\n"
            
            content += "Note: This is a basic response. Enhanced Gemini reasoning is not available."
        else:
            content = f"I don't have enough information to answer: {query}"
        
        return GeminiResponse(
            content=content,
            model="fallback",
            timestamp=datetime.now(timezone.utc),
            usage_metadata={},
            confidence=0.3
        )
    
    def _extract_answer_from_response(self, response_content: str) -> str:
        """Extract the main answer from Gemini response"""
        # Simple extraction - can be enhanced with more sophisticated parsing
        lines = response_content.split('\n')
        
        # Look for answer section
        answer_start = -1
        for i, line in enumerate(lines):
            if any(marker in line.lower() for marker in ['answer:', 'response:', 'conclusion:']):
                answer_start = i + 1
                break
        
        if answer_start > -1:
            return '\n'.join(lines[answer_start:]).strip()
        else:
            return response_content.strip()
    
    def _extract_reasoning_chain(self, response_content: str) -> List[str]:
        """Extract reasoning steps from Gemini response"""
        reasoning_steps = []
        lines = response_content.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for numbered steps or bullet points
            if any(line.startswith(marker) for marker in ['1.', '2.', '3.', '-', '*', '•']):
                reasoning_steps.append(line)
            elif line.startswith('Step ') or line.startswith('Reasoning:'):
                reasoning_steps.append(line)
        
        return reasoning_steps[:10]  # Limit to prevent clutter
    
    def _extract_source_citations(self, rag_context: RAGContext, enhanced_answer: str) -> List[Dict[str, str]]:
        """Extract source citations from context and answer"""
        citations = []
        
        for i, result in enumerate(rag_context.retrieved_documents):
            doc = result.document
            
            # Check if source is referenced in answer
            is_referenced = any(
                term in enhanced_answer.lower() 
                for term in result.highlighted_terms
            ) if result.highlighted_terms else True
            
            if is_referenced:
                citation = {
                    "source_id": f"source_{i+1}",
                    "title": doc.source or f"Document {doc.id[:8]}",
                    "type": doc.doc_type.value,
                    "relevance": f"{result.similarity_score:.3f}",
                    "snippet": result.context_snippet
                }
                citations.append(citation)
        
        return citations
    
    def _calculate_enhanced_confidence(self,
                                     rag_context: RAGContext,
                                     gemini_response: GeminiResponse,
                                     reasoning_chain: List[str]) -> float:
        """Calculate confidence score for enhanced result"""
        # Base confidence from RAG context
        rag_confidence = rag_context.confidence_score
        
        # Gemini response confidence
        gemini_confidence = gemini_response.confidence
        
        # Reasoning quality bonus
        reasoning_bonus = min(len(reasoning_chain) * 0.05, 0.2)
        
        # Combined confidence (weighted average)
        combined_confidence = (
            rag_confidence * 0.4 +
            gemini_confidence * 0.4 +
            reasoning_bonus * 0.2
        )
        
        return min(combined_confidence, 1.0)
    
    def _create_fallback_result(self, query: str, error_msg: str) -> EnhancedRAGResult:
        """Create fallback result for error cases"""
        from .core import RAGContext
        
        empty_context = RAGContext(
            query=query,
            retrieved_documents=[],
            context_window="",
            total_tokens=0,
            confidence_score=0.0,
            retrieval_method="error",
            timestamp=datetime.now(timezone.utc)
        )
        
        error_response = GeminiResponse(
            content=f"Error processing query: {error_msg}",
            model="error",
            timestamp=datetime.now(timezone.utc),
            usage_metadata={},
            confidence=0.0
        )
        
        return EnhancedRAGResult(
            query=query,
            rag_context=empty_context,
            gemini_response=error_response,
            enhanced_answer=f"I encountered an error processing your query: {error_msg}",
            confidence_score=0.0,
            reasoning_chain=[],
            source_citations=[],
            timestamp=datetime.now(timezone.utc)
        )
    
    # Response templates
    def _get_direct_template(self) -> str:
        return """You are an AI assistant with access to relevant documentation and code.
        
Query: {query}

Relevant Context ({num_sources} sources, confidence: {confidence:.2f}):
{context}

Provide a direct, concise answer based on the context above. If the context doesn't contain enough information, clearly state what information is missing.

Answer:"""
    
    def _get_reasoning_template(self) -> str:
        return """You are an AI assistant that provides step-by-step reasoning.

Query: {query}

Relevant Context ({num_sources} sources, confidence: {confidence:.2f}):
{context}

Please provide a reasoned response following this structure:
1. Analysis of the query
2. Key information from the context
3. Step-by-step reasoning
4. Conclusion/Answer

Reasoning:"""
    
    def _get_synthesis_template(self) -> str:
        return """You are an AI assistant that synthesizes information from multiple sources.

Query: {query}

Relevant Context ({num_sources} sources, confidence: {confidence:.2f}):
{context}

Synthesize the information from the sources above to provide a comprehensive answer. Note any contradictions or gaps in the information.

Synthesis:"""
    
    def _get_analysis_template(self) -> str:
        return """You are an AI assistant that provides analytical breakdowns.

Query: {query}

Relevant Context ({num_sources} sources, confidence: {confidence:.2f}):
{context}

Provide an analytical breakdown of the query based on the context:
- Key components and concepts
- Relationships and dependencies  
- Implications and considerations
- Recommendations or next steps

Analysis:"""
    
    def _get_creative_template(self) -> str:
        return """You are a creative AI assistant that provides innovative solutions.

Query: {query}

Relevant Context ({num_sources} sources, confidence: {confidence:.2f}):
{context}

Using the context as a foundation, provide creative and innovative approaches to address the query. Think outside the box while staying grounded in the available information.

Creative Response:"""
    
    async def batch_process_queries(self, 
                                  queries: List[str],
                                  response_mode: ResponseMode = ResponseMode.REASONING) -> List[EnhancedRAGResult]:
        """Process multiple queries in batch"""
        results = []
        
        for query in queries:
            try:
                result = await self.enhanced_query(query, response_mode)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch processing failed for query '{query}': {e}")
                results.append(self._create_fallback_result(query, str(e)))
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Gemini RAG integration statistics"""
        rag_stats = self.rag_system.get_stats()
        
        return {
            "rag_system": rag_stats,
            "gemini_model": self.model_name,
            "gemini_available": GEMINI_AVAILABLE,
            "max_context_length": self.max_context_length,
            "temperature": self.temperature,
            "response_modes": [mode.value for mode in ResponseMode]
        }


# Factory function for easy initialization
def create_gemini_rag_system(
    rag_system: RAGSystem,
    gemini_api_key: Optional[str] = None,
    model: str = GeminiModel.GEMINI_PRO.value
) -> GeminiRAGIntegration:
    """Create Gemini-enhanced RAG system"""
    return GeminiRAGIntegration(rag_system, gemini_api_key, model)


# Example usage and testing
async def main():
    """Example usage of Gemini RAG integration"""
    
    # Initialize RAG system (reuse from core module)
    from .core import create_rag_system, DocumentType
    
    rag = create_rag_system()
    
    # Add sample documents
    await rag.add_document(
        "Digital twin cognitive modeling tracks agent states and predicts behavior patterns.",
        DocumentType.DOCUMENTATION,
        {"topic": "cognitive_modeling"},
        "cognitive_docs.md"
    )
    
    # Initialize Gemini integration (without API key for demo)
    gemini_rag = create_gemini_rag_system(rag)
    
    # Process enhanced query
    result = await gemini_rag.enhanced_query(
        "How does cognitive modeling work in digital twins?",
        ResponseMode.REASONING
    )
    
    print(f"Enhanced Query Result:")
    print(f"Confidence: {result.confidence_score:.3f}")
    print(f"Sources: {len(result.source_citations)}")
    print(f"Answer: {result.enhanced_answer[:200]}...")
    print(f"Reasoning steps: {len(result.reasoning_chain)}")
    
    # Display statistics
    stats = gemini_rag.get_stats()
    print(f"\nGemini RAG Stats: {stats}")
    
    print("Gemini RAG integration demonstration complete!")


if __name__ == "__main__":
    asyncio.run(main())
