"""
RAG System Implementation for AI Qube Centaur System
Integrates with your existing agent framework and Weaviate setup
"""

import asyncio
import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import weaviate
from sentence_transformers import SentenceTransformer
import openai
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class KnowledgeDocument:
    """Structure for knowledge documents in the RAG system"""
    id: str
    content: str
    metadata: Dict[str, Any]
    source: str
    doc_type: str
    embedding: Optional[List[float]] = None

class CentaurRAGSystem:
    """RAG system specifically designed for Centaur multi-agent coordination"""
    
    def __init__(self, weaviate_url: str = "http://localhost:8080"):
        self.client = weaviate.Client(weaviate_url)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.class_name = "CentaurKnowledge"
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Initialize Weaviate schema for Centaur knowledge"""
        schema = {
            "class": self.class_name,
            "description": "Knowledge base for Centaur multi-agent coordination",
            "vectorizer": "none",  # We'll provide our own vectors
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "Main content of the document"
                },
                {
                    "name": "source",
                    "dataType": ["string"],
                    "description": "Source of the document"
                },
                {
                    "name": "doc_type",
                    "dataType": ["string"],
                    "description": "Type of document (architecture, agent_pattern, task_history, etc.)"
                },
                {
                    "name": "agent_context",
                    "dataType": ["string"],
                    "description": "Which agents this knowledge is relevant for"
                },
                {
                    "name": "complexity_level",
                    "dataType": ["string"],
                    "description": "Complexity level: basic, intermediate, advanced"
                },
                {
                    "name": "success_metrics",
                    "dataType": ["object"],
                    "description": "Performance metrics if applicable"
                },
                {
                    "name": "timestamp",
                    "dataType": ["date"],
                    "description": "When this knowledge was created or updated"
                }
            ]
        }
        
        # Create class if it doesn't exist
        try:
            if not self.client.schema.exists(self.class_name):
                self.client.schema.create_class(schema)
                logger.info(f"Created Weaviate class: {self.class_name}")
        except Exception as e:
            logger.error(f"Error creating schema: {e}")
    
    async def index_centaur_documentation(self) -> int:
        """Index all Centaur system documentation"""
        documents = []
        
        # Index architectural documentation
        arch_docs = await self._extract_architectural_knowledge()
        documents.extend(arch_docs)
        
        # Index agent coordination patterns
        coordination_docs = await self._extract_coordination_patterns()
        documents.extend(coordination_docs)
        
        # Index successful task patterns
        task_docs = await self._extract_task_patterns()
        documents.extend(task_docs)
        
        # Index development guidelines
        guideline_docs = await self._extract_development_guidelines()
        documents.extend(guideline_docs)
        
        # Batch insert documents
        indexed_count = 0
        for doc in documents:
            try:
                # Generate embedding
                doc.embedding = self.embedding_model.encode(doc.content).tolist()
                
                # Insert into Weaviate
                self.client.data_object.create(
                    data_object={
                        "content": doc.content,
                        "source": doc.source,
                        "doc_type": doc.doc_type,
                        "agent_context": doc.metadata.get("agent_context", "all"),
                        "complexity_level": doc.metadata.get("complexity_level", "intermediate"),
                        "success_metrics": doc.metadata.get("success_metrics", {}),
                        "timestamp": doc.metadata.get("timestamp", "2025-06-11T00:00:00Z")
                    },
                    class_name=self.class_name,
                    vector=doc.embedding,
                    uuid=doc.id
                )
                indexed_count += 1
                
            except Exception as e:
                logger.error(f"Error indexing document {doc.id}: {e}")
        
        logger.info(f"Indexed {indexed_count} documents into Centaur knowledge base")
        return indexed_count
    
    async def _extract_architectural_knowledge(self) -> List[KnowledgeDocument]:
        """Extract knowledge from architectural documentation"""
        docs = []
        
        # Architecture patterns from your excellent documentation
        architecture_knowledge = [
            {
                "content": """Trifinity Orchestration Matrix (TOM) Architecture:
                - Claude 4 Opus: Strategic Architect & Code Quality Lead
                - OpenAI Codex: Implementation Specialist  
                - Gemini 2.5 Pro: Research & Optimization Engine
                
                Coordination Pattern: Strategic Analysis → Implementation → Optimization
                Success Metrics: 10-20x development velocity, 90%+ quality scores""",
                "doc_type": "architecture",
                "agent_context": "claude,codex,gemini",
                "complexity_level": "advanced"
            },
            {
                "content": """Agent Capability-Based Task Assignment:
                - Analyze task requirements and extract required capabilities
                - Match capabilities to agent strengths using capability intersection scoring
                - Consider current workload and availability
                - Assign to agent with highest capability score and lowest workload
                
                Implementation: AgentCoordinationFramework.find_best_agent()""",
                "doc_type": "coordination_pattern",
                "agent_context": "all",
                "complexity_level": "intermediate"
            },
            {
                "content": """Recursive Improvement Architecture:
                1. Performance Monitoring: Track agent coordination effectiveness
                2. Pattern Discovery: Identify successful collaboration patterns  
                3. Architecture Evolution: Modify coordination mechanisms
                4. Meta-Learning: Improve the improvement process itself
                
                Key Principle: System learns better ways to coordinate agents""",
                "doc_type": "recursive_learning",
                "agent_context": "all", 
                "complexity_level": "advanced"
            }
        ]
        
        for i, knowledge in enumerate(architecture_knowledge):
            docs.append(KnowledgeDocument(
                id=f"arch_{i}",
                content=knowledge["content"],
                metadata={
                    "agent_context": knowledge["agent_context"],
                    "complexity_level": knowledge["complexity_level"],
                    "timestamp": "2025-06-11T00:00:00Z"
                },
                source="centaur_architecture",
                doc_type=knowledge["doc_type"]
            ))
        
        return docs
    
    async def _extract_coordination_patterns(self) -> List[KnowledgeDocument]:
        """Extract successful agent coordination patterns"""
        docs = []
        
        coordination_patterns = [
            {
                "content": """Successful 2-Agent Coordination Pattern (Claude + Codex):
                1. Claude analyzes requirements and creates architectural plan
                2. Claude broadcasts plan to Codex with structured context
                3. Codex implements based on architectural guidance
                4. Results synthesized with quality metrics tracked
                
                Success Rate: 100% in initial testing
                Average Coordination Time: <1 hour response time""",
                "pattern_type": "two_agent_coordination",
                "agents": ["claude", "codex"],
                "success_metrics": {"completion_rate": 1.0, "response_time": 3600}
            },
            {
                "content": """Message Protocol for Agent Communication:
                - Use AgentMessage with sender, recipient, task_id, priority
                - Include correlation_id for tracking conversation threads
                - Set appropriate priority levels (critical, high, medium, low)
                - Always include context and required_response flag
                
                Critical: All inter-agent communication must use standardized format""",
                "pattern_type": "communication_protocol",
                "agents": ["all"],
                "success_metrics": {"message_delivery_rate": 1.0, "format_compliance": 1.0}
            }
        ]
        
        for i, pattern in enumerate(coordination_patterns):
            docs.append(KnowledgeDocument(
                id=f"coord_{i}",
                content=pattern["content"],
                metadata={
                    "agent_context": ",".join(pattern["agents"]),
                    "success_metrics": pattern["success_metrics"],
                    "timestamp": "2025-06-11T00:00:00Z"
                },
                source="coordination_patterns",
                doc_type=pattern["pattern_type"]
            ))
        
        return docs
    
    async def _extract_task_patterns(self) -> List[KnowledgeDocument]:
        """Extract successful task execution patterns"""
        # This would extract from your task history database
        # For now, using example patterns
        return []
    
    async def _extract_development_guidelines(self) -> List[KnowledgeDocument]:
        """Extract development guidelines and best practices"""
        docs = []
        
        guidelines = [
            {
                "content": """Code Quality Standards for Centaur System:
                - All agent-generated code must include comprehensive error handling
                - Use async/await patterns for agent communication
                - Include proper type hints and docstrings
                - Implement comprehensive logging for debugging
                - Follow the BaseAgent abstract class pattern
                
                Quality Gate: 100% test coverage for coordination logic""",
                "guideline_type": "code_quality"
            },
            {
                "content": """Agent Task Assignment Best Practices:
                - Always check agent availability before assignment
                - Consider task complexity vs agent capability scores
                - Implement graceful degradation if preferred agent unavailable
                - Track performance metrics for continuous improvement
                - Use capability intersection scoring for optimal assignment""",
                "guideline_type": "task_assignment"
            }
        ]
        
        for i, guideline in enumerate(guidelines):
            docs.append(KnowledgeDocument(
                id=f"guide_{i}",
                content=guideline["content"],
                metadata={
                    "agent_context": "all",
                    "timestamp": "2025-06-11T00:00:00Z"
                },
                source="development_guidelines",
                doc_type=guideline["guideline_type"]
            ))
        
        return docs
    
    async def query_contextual_knowledge(self, 
                                       query: str, 
                                       agent_context: str = "all",
                                       task_type: str = None,
                                       limit: int = 5) -> List[Dict[str, Any]]:
        """Query relevant knowledge for agent coordination"""
        
        # Generate query embedding
        query_vector = self.embedding_model.encode(query).tolist()
        
        # Build where filter
        where_filter = {"path": ["agent_context"], "operator": "ContainsAny", "valueStringArray": [agent_context, "all"]}
        
        if task_type:
            where_filter = {
                "operator": "And",
                "operands": [
                    where_filter,
                    {"path": ["doc_type"], "operator": "Equal", "valueString": task_type}
                ]
            }
        
        # Perform similarity search
        try:
            result = (
                self.client.query
                .get(self.class_name, ["content", "source", "doc_type", "agent_context", "success_metrics"])
                .with_near_vector({"vector": query_vector})
                .with_where(where_filter)
                .with_limit(limit)
                .with_additional(["distance", "id"])
                .do()
            )
            
            if "data" in result and "Get" in result["data"]:
                return result["data"]["Get"][self.class_name]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error querying knowledge: {e}")
            return []
    
    async def enhance_agent_context(self, 
                                  task_description: str,
                                  assigned_agents: List[str]) -> Dict[str, Any]:
        """Enhance agent context with relevant knowledge from RAG"""
        
        enhanced_context = {
            "task_description": task_description,
            "relevant_patterns": [],
            "architectural_guidance": [],
            "success_metrics": {},
            "coordination_advice": []
        }
        
        # Query for relevant coordination patterns
        coordination_knowledge = await self.query_contextual_knowledge(
            query=task_description,
            agent_context=",".join(assigned_agents),
            task_type="coordination_pattern"
        )
        enhanced_context["relevant_patterns"] = coordination_knowledge
        
        # Query for architectural guidance
        arch_knowledge = await self.query_contextual_knowledge(
            query=task_description,
            agent_context=",".join(assigned_agents),
            task_type="architecture"
        )
        enhanced_context["architectural_guidance"] = arch_knowledge
        
        # Extract success metrics from similar tasks
        for knowledge in coordination_knowledge + arch_knowledge:
            if "success_metrics" in knowledge:
                enhanced_context["success_metrics"].update(knowledge["success_metrics"])
        
        return enhanced_context
    
    async def learn_from_coordination_outcome(self,
                                            task_id: str,
                                            coordination_pattern: Dict[str, Any],
                                            outcome_metrics: Dict[str, Any]) -> None:
        """Learn from coordination outcomes to improve future performance"""
        
        # Create new knowledge document from successful coordination
        if outcome_metrics.get("success_rate", 0) > 0.8:
            new_knowledge = KnowledgeDocument(
                id=f"learned_{task_id}",
                content=f"""Successful Coordination Pattern:
                Task: {coordination_pattern['task_description']}
                Agents: {coordination_pattern['assigned_agents']}
                Pattern: {coordination_pattern['execution_pattern']}
                Success Metrics: {outcome_metrics}
                
                Key Success Factors: {coordination_pattern.get('success_factors', [])}""",
                metadata={
                    "agent_context": ",".join(coordination_pattern['assigned_agents']),
                    "success_metrics": outcome_metrics,
                    "timestamp": coordination_pattern.get('timestamp', "2025-06-11T00:00:00Z"),
                    "learned_from_task": task_id
                },
                source="coordination_learning",
                doc_type="learned_pattern"
            )
            
            # Generate embedding and store
            new_knowledge.embedding = self.embedding_model.encode(new_knowledge.content).tolist()
            
            try:
                self.client.data_object.create(
                    data_object={
                        "content": new_knowledge.content,
                        "source": new_knowledge.source,
                        "doc_type": new_knowledge.doc_type,
                        "agent_context": new_knowledge.metadata["agent_context"],
                        "complexity_level": "learned",
                        "success_metrics": new_knowledge.metadata["success_metrics"],
                        "timestamp": new_knowledge.metadata["timestamp"]
                    },
                    class_name=self.class_name,
                    vector=new_knowledge.embedding,
                    uuid=new_knowledge.id
                )
                
                logger.info(f"Learned new coordination pattern from task {task_id}")
                
            except Exception as e:
                logger.error(f"Error storing learned pattern: {e}")
    
    async def get_system_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            # Get total count
            result = self.client.query.aggregate(self.class_name).with_meta_count().do()
            total_count = result["data"]["Aggregate"][self.class_name][0]["meta"]["count"]
            
            # Get count by document type
            doc_type_stats = {}
            for doc_type in ["architecture", "coordination_pattern", "learned_pattern", "code_quality"]:
                type_result = (
                    self.client.query.aggregate(self.class_name)
                    .with_where({"path": ["doc_type"], "operator": "Equal", "valueString": doc_type})
                    .with_meta_count()
                    .do()
                )
                if type_result["data"]["Aggregate"][self.class_name]:
                    doc_type_stats[doc_type] = type_result["data"]["Aggregate"][self.class_name][0]["meta"]["count"]
                else:
                    doc_type_stats[doc_type] = 0
            
            return {
                "total_documents": total_count,
                "document_types": doc_type_stats,
                "status": "operational"
            }
            
        except Exception as e:
            logger.error(f"Error getting knowledge stats: {e}")
            return {"status": "error", "error": str(e)}

# Integration with existing agent framework
async def integrate_rag_with_agent_framework():
    """Integration example with your existing AgentCoordinationFramework"""
    
    rag_system = CentaurRAGSystem()
    
    # Index initial knowledge
    await rag_system.index_centaur_documentation()
    
    # Example: Enhanced agent coordination with RAG
    async def enhanced_assign_task(framework, task_id: str, agent_id: str = None):
        """Enhanced version of your assign_task method with RAG integration"""
        
        task = framework.tasks[task_id]
        
        # Get enhanced context from RAG
        enhanced_context = await rag_system.enhance_agent_context(
            task_description=task.description,
            assigned_agents=[agent_id] if agent_id else []
        )
        
        # Add RAG context to task
        task.context.update({
            "rag_context": enhanced_context,
            "relevant_patterns": enhanced_context["relevant_patterns"],
            "architectural_guidance": enhanced_context["architectural_guidance"]
        })
        
        # Proceed with normal task assignment
        result = await framework.assign_task(task_id, agent_id)
        
        return result

# Example usage
async def test_rag_system():
    """Test the RAG system integration"""
    
    rag = CentaurRAGSystem()
    
    # Index knowledge
    indexed_count = await rag.index_centaur_documentation()
    print(f"Indexed {indexed_count} documents")
    
    # Test querying
    results = await rag.query_contextual_knowledge(
        query="How should I coordinate Claude and Codex for a Python implementation task?",
        agent_context="claude,codex"
    )
    
    print("RAG Query Results:")
    for result in results:
        print(f"- {result['content'][:100]}...")
    
    # Test context enhancement
    enhanced = await rag.enhance_agent_context(
        task_description="Create a Python function for data processing with error handling",
        assigned_agents=["claude", "codex"]
    )
    
    print(f"Enhanced context includes {len(enhanced['relevant_patterns'])} patterns")

if __name__ == "__main__":
    asyncio.run(test_rag_system())