"""
Digital Twin API Interface
CENTAUR-012: REST API endpoints for digital twin interaction

Provides HTTP endpoints for:
- Agent state monitoring
- Cognitive metrics tracking  
- Coordination recommendations
- Real-time digital twin updates
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import logging

from .cognitive_core import (
    DigitalTwinEngine, 
    CognitiveState, 
    AgentType,
    create_digital_twin_engine
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Digital Twin API",
    description="AI Qube Centaur Ecosystem Digital Twin Interface",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global digital twin engine instance
digital_twin: Optional[DigitalTwinEngine] = None

# Pydantic models for API requests/responses
class AgentStateUpdate(BaseModel):
    """Request model for agent state updates"""
    agent_id: str
    new_state: str  # CognitiveState enum value
    metrics: Optional[Dict[str, float]] = None

class AgentStateResponse(BaseModel):
    """Response model for agent state queries"""
    agent_id: str
    agent_type: str
    current_state: str
    predicted_next_state: Optional[str]
    confidence_score: float
    last_updated: datetime
    task_queue_size: int
    active_tasks: List[str]
    processing_load: float
    memory_usage: float
    success_rate: float

class CoordinationRecommendation(BaseModel):
    """Model for coordination recommendations"""
    type: str
    priority: str
    message: str
    suggested_action: str
    timestamp: str
    agent_id: Optional[str] = None
    idle_agents: Optional[List[str]] = None
    active_agents: Optional[List[str]] = None

@app.on_event("startup")
async def startup_event():
    """Initialize digital twin engine on startup"""
    global digital_twin
    try:
        digital_twin = create_digital_twin_engine()
        logger.info("Digital Twin API started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize digital twin engine: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Digital Twin API shutting down")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Digital Twin API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "agents": "/agents",
            "agent_state": "/agents/{agent_id}",
            "update_state": "/agents/{agent_id}/state",
            "coordination": "/coordination/recommendations",
            "export": "/export"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if digital_twin is None:
        raise HTTPException(status_code=503, detail="Digital twin engine not initialized")
    
    try:
        # Get current agent states to verify engine is working
        states = await digital_twin.get_all_states()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "active_agents": len(states),
            "engine_status": "operational"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Engine error: {str(e)}")

@app.get("/agents", response_model=Dict[str, AgentStateResponse])
async def get_all_agents():
    """Get all agent digital twin states"""
    if digital_twin is None:
        raise HTTPException(status_code=503, detail="Digital twin engine not initialized")
    
    try:
        states = await digital_twin.get_all_states()
        response = {}
        
        for agent_id, state in states.items():
            response[agent_id] = AgentStateResponse(
                agent_id=state.agent_id,
                agent_type=state.agent_type.value,
                current_state=state.current_state.value,
                predicted_next_state=state.predicted_next_state.value if state.predicted_next_state else None,
                confidence_score=state.confidence_score,
                last_updated=state.last_updated,
                task_queue_size=state.task_queue_size,
                active_tasks=state.active_tasks,
                processing_load=state.metrics.processing_load,
                memory_usage=state.metrics.memory_usage,
                success_rate=state.metrics.success_rate
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to get agent states: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_id}", response_model=AgentStateResponse)
async def get_agent_state(agent_id: str):
    """Get specific agent digital twin state"""
    if digital_twin is None:
        raise HTTPException(status_code=503, detail="Digital twin engine not initialized")
    
    try:
        state = await digital_twin.get_agent_state(agent_id)
        if state is None:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        return AgentStateResponse(
            agent_id=state.agent_id,
            agent_type=state.agent_type.value,
            current_state=state.current_state.value,
            predicted_next_state=state.predicted_next_state.value if state.predicted_next_state else None,
            confidence_score=state.confidence_score,
            last_updated=state.last_updated,
            task_queue_size=state.task_queue_size,
            active_tasks=state.active_tasks,
            processing_load=state.metrics.processing_load,
            memory_usage=state.metrics.memory_usage,
            success_rate=state.metrics.success_rate
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent state for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/{agent_id}/state")
async def update_agent_state(agent_id: str, update: AgentStateUpdate):
    """Update agent cognitive state"""
    if digital_twin is None:
        raise HTTPException(status_code=503, detail="Digital twin engine not initialized")
    
    try:
        # Validate state enum
        try:
            new_state = CognitiveState(update.new_state)
        except ValueError:
            valid_states = [state.value for state in CognitiveState]
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid state '{update.new_state}'. Valid states: {valid_states}"
            )
        
        # Update the agent state
        success = await digital_twin.update_agent_state(
            agent_id=agent_id,
            new_state=new_state,
            metrics=update.metrics
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to update agent state")
        
        # Return updated state
        updated_state = await digital_twin.get_agent_state(agent_id)
        if updated_state is None:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found after update")
        
        return {
            "success": True,
            "message": f"Agent {agent_id} state updated to {new_state.value}",
            "timestamp": datetime.now().isoformat(),
            "state": AgentStateResponse(
                agent_id=updated_state.agent_id,
                agent_type=updated_state.agent_type.value,
                current_state=updated_state.current_state.value,
                predicted_next_state=updated_state.predicted_next_state.value if updated_state.predicted_next_state else None,
                confidence_score=updated_state.confidence_score,
                last_updated=updated_state.last_updated,
                task_queue_size=updated_state.task_queue_size,
                active_tasks=updated_state.active_tasks,
                processing_load=updated_state.metrics.processing_load,
                memory_usage=updated_state.metrics.memory_usage,
                success_rate=updated_state.metrics.success_rate
            )
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update agent state for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/coordination/recommendations", response_model=List[CoordinationRecommendation])
async def get_coordination_recommendations():
    """Get current coordination recommendations"""
    if digital_twin is None:
        raise HTTPException(status_code=503, detail="Digital twin engine not initialized")
    
    try:
        recommendations = await digital_twin.get_coordination_recommendations()
        
        response = []
        for rec in recommendations:
            response.append(CoordinationRecommendation(
                type=rec["type"],
                priority=rec["priority"],
                message=rec["message"],
                suggested_action=rec["suggested_action"],
                timestamp=rec["timestamp"],
                agent_id=rec.get("agent_id"),
                idle_agents=rec.get("idle_agents"),
                active_agents=rec.get("active_agents")
            ))
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to get coordination recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export")
async def export_digital_twin_state():
    """Export complete digital twin state as JSON"""
    if digital_twin is None:
        raise HTTPException(status_code=503, detail="Digital twin engine not initialized")
    
    try:
        state_json = await digital_twin.export_state()
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "data": state_json
        }
        
    except Exception as e:
        logger.error(f"Failed to export digital twin state: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate/{agent_id}")
async def simulate_agent_workload(agent_id: str, duration_seconds: int = 60):
    """Simulate agent workload for testing purposes"""
    if digital_twin is None:
        raise HTTPException(status_code=503, detail="Digital twin engine not initialized")
    
    try:
        # Start background simulation
        asyncio.create_task(_simulate_workload(agent_id, duration_seconds))
        
        return {
            "success": True,
            "message": f"Started workload simulation for {agent_id}",
            "duration": duration_seconds,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start simulation for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def _simulate_workload(agent_id: str, duration_seconds: int):
    """Background task to simulate agent workload"""
    try:
        import random
        
        start_time = datetime.now().timestamp()
        end_time = start_time + duration_seconds
        
        # Simulate processing state
        await digital_twin.update_agent_state(
            agent_id,
            CognitiveState.PROCESSING,
            {
                "processing_load": 0.7,
                "task_complexity": 0.8,
                "memory_usage": 0.6
            }
        )
        
        # Simulate varying workload
        while datetime.now().timestamp() < end_time:
            load = random.uniform(0.3, 0.9)
            complexity = random.uniform(0.2, 1.0)
            
            await digital_twin.update_agent_state(
                agent_id,
                CognitiveState.PROCESSING,
                {
                    "processing_load": load,
                    "task_complexity": complexity,
                    "response_time": random.uniform(0.1, 2.0)
                }
            )
            
            await asyncio.sleep(5)  # Update every 5 seconds
        
        # Return to idle
        await digital_twin.update_agent_state(
            agent_id,
            CognitiveState.IDLE,
            {
                "processing_load": 0.1,
                "task_complexity": 0.0,
                "memory_usage": 0.2
            }
        )
        
        logger.info(f"Simulation completed for {agent_id}")
        
    except Exception as e:
        logger.error(f"Simulation failed for {agent_id}: {e}")

# Development server startup
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
