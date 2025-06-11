"""
Digital Twin Module
CENTAUR-012: Digital Twin API + Codex Integration

This module provides cognitive state modeling and digital twin functionality
for the AI Qube Centaur Ecosystem.

Key Components:
- CognitiveCore: Core digital twin engine with state tracking
- API: REST API interface for digital twin interaction
- Integration: OpenAI Codex integration for advanced predictions

Usage:
    from digital_twin import create_digital_twin_engine, DigitalTwinEngine
    
    # Initialize engine
    engine = create_digital_twin_engine()
    
    # Update agent state
    await engine.update_agent_state("agent_id", CognitiveState.PROCESSING)
"""

from .cognitive_core import (
    DigitalTwinEngine,
    CognitiveState,
    AgentType,
    CognitiveMetrics,
    DigitalTwinState,
    create_digital_twin_engine
)

from .api import app as digital_twin_api

__version__ = "1.0.0"
__author__ = "AI Qube Centaur Ecosystem"

__all__ = [
    "DigitalTwinEngine",
    "CognitiveState", 
    "AgentType",
    "CognitiveMetrics",
    "DigitalTwinState",
    "create_digital_twin_engine",
    "digital_twin_api"
]

# Module level convenience functions
def start_digital_twin_api(host: str = "0.0.0.0", port: int = 8000):
    """Start the Digital Twin API server"""
    import uvicorn
    uvicorn.run(digital_twin_api, host=host, port=port, log_level="info")

def create_engine_with_config(config_path: str) -> DigitalTwinEngine:
    """Create engine with custom configuration"""
    return create_digital_twin_engine(config_path)
