"""
Configuration management for the Centaur System
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Core Application Settings
    environment: str = Field(default="development", env="NODE_ENV")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="info", env="LOG_LEVEL")
    port: int = Field(default=8000, env="PORT")
    
    # Database Configuration
    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(..., env="REDIS_URL")
    
    # AI Agent API Keys
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    google_ai_api_key: str = Field(..., env="GOOGLE_AI_API_KEY")
    
    # AI Model Configuration
    claude_model: str = Field(default="claude-3-opus-20240229", env="CLAUDE_MODEL")
    openai_model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    gemini_model: str = Field(default="gemini-pro", env="GEMINI_MODEL")
    
    # n8n Configuration
    n8n_host: str = Field(default="localhost", env="N8N_HOST")
    n8n_port: int = Field(default=5678, env="N8N_PORT")
    n8n_protocol: str = Field(default="http", env="N8N_PROTOCOL")
    n8n_webhook_url: str = Field(default="http://localhost:5678/webhook", env="N8N_WEBHOOK_URL")
    
    # Vector Database Configuration
    pinecone_api_key: Optional[str] = Field(default=None, env="PINECONE_API_KEY")
    pinecone_environment: Optional[str] = Field(default=None, env="PINECONE_ENVIRONMENT")
    pinecone_index_name: str = Field(default="centaur-knowledge-base", env="PINECONE_INDEX_NAME")
    
    weaviate_url: str = Field(default="http://localhost:8080", env="WEAVIATE_URL")
    weaviate_api_key: Optional[str] = Field(default=None, env="WEAVIATE_API_KEY")
    
    # Security Configuration
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_expiration: str = Field(default="24h", env="JWT_EXPIRATION")
    bcrypt_rounds: int = Field(default=12, env="BCRYPT_ROUNDS")
    
    # Recursive Improvement Engine
    improvement_cycle_interval: int = Field(default=86400, env="IMPROVEMENT_CYCLE_INTERVAL")  # 24 hours
    performance_threshold: float = Field(default=0.85, env="PERFORMANCE_THRESHOLD")
    meta_learning_enabled: bool = Field(default=True, env="META_LEARNING_ENABLED")
    architecture_evolution_enabled: bool = Field(default=True, env="ARCHITECTURE_EVOLUTION_ENABLED")
    
    # Agent Coordination Settings
    max_concurrent_tasks: int = Field(default=10, env="MAX_CONCURRENT_TASKS")
    task_timeout: int = Field(default=3600, env="TASK_TIMEOUT")  # 1 hour
    coordination_check_interval: int = Field(default=30, env="COORDINATION_CHECK_INTERVAL")
    
    # RAG System Configuration
    rag_chunk_size: int = Field(default=1000, env="RAG_CHUNK_SIZE")
    rag_chunk_overlap: int = Field(default=200, env="RAG_CHUNK_OVERLAP")
    rag_similarity_threshold: float = Field(default=0.7, env="RAG_SIMILARITY_THRESHOLD")
    rag_max_results: int = Field(default=10, env="RAG_MAX_RESULTS")
    
    # Performance Configuration
    max_workers: int = Field(default=4, env="MAX_WORKERS")
    worker_timeout: int = Field(default=30, env="WORKER_TIMEOUT")
    connection_pool_size: int = Field(default=20, env="CONNECTION_POOL_SIZE")
    
    # Development Settings
    mock_ai_responses: bool = Field(default=False, env="MOCK_AI_RESPONSES")
    enable_debug_logging: bool = Field(default=True, env="ENABLE_DEBUG_LOGGING")
    save_interaction_logs: bool = Field(default=True, env="SAVE_INTERACTION_LOGS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_configuration()
    
    def _validate_configuration(self):
        """Validate configuration settings"""
        # Validate required API keys in production
        if self.environment == "production":
            required_keys = [
                self.anthropic_api_key,
                self.openai_api_key,
                self.google_ai_api_key,
                self.jwt_secret
            ]
            if not all(required_keys):
                raise ValueError("Missing required API keys for production environment")
        
        # Validate database URLs
        if not self.database_url.startswith(('postgresql://', 'postgres://')):
            raise ValueError("Invalid database URL format")
        
        if not self.redis_url.startswith('redis://'):
            raise ValueError("Invalid Redis URL format")
    
    @property
    def n8n_base_url(self) -> str:
        """Get the base n8n URL"""
        return f"{self.n8n_protocol}://{self.n8n_host}:{self.n8n_port}"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment == "production"
