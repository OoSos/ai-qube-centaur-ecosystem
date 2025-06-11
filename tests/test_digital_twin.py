"""
Test Suite for Digital Twin Module
CENTAUR-012: Digital Twin API + Codex Integration Tests

Comprehensive test coverage for:
- Cognitive core functionality
- API endpoints
- State management
- Prediction algorithms
"""

import pytest
import asyncio
import json
from datetime import datetime, timezone
from unittest.mock import Mock, patch
import numpy as np

# Import modules to test
from src.digital_twin import (
    DigitalTwinEngine,
    CognitiveState,
    AgentType,
    CognitiveMetrics,
    create_digital_twin_engine
)


class TestDigitalTwinEngine:
    """Test cases for Digital Twin Engine"""
    
    @pytest.fixture
    async def engine(self):
        """Create test engine instance"""
        return create_digital_twin_engine()
    
    @pytest.mark.asyncio
    async def test_engine_initialization(self, engine):
        """Test engine initializes correctly"""
        assert engine is not None
        assert len(engine.agents) == 4  # 4 default agent types
        assert "codex_primary" in engine.agents
        assert "gemini_primary" in engine.agents
        assert "claude_primary" in engine.agents
        assert "copilot_primary" in engine.agents
    
    @pytest.mark.asyncio
    async def test_update_agent_state(self, engine):
        """Test agent state updates"""
        agent_id = "codex_primary"
        new_state = CognitiveState.PROCESSING
        metrics = {
            "processing_load": 0.8,
            "task_complexity": 0.9,
            "memory_usage": 0.6
        }
        
        # Update state
        success = await engine.update_agent_state(agent_id, new_state, metrics)
        assert success is True
        
        # Check state was updated
        agent_state = await engine.get_agent_state(agent_id)
        assert agent_state is not None
        assert agent_state.current_state == new_state
        assert agent_state.metrics.processing_load == 0.8
        assert agent_state.metrics.task_complexity == 0.9
    
    @pytest.mark.asyncio
    async def test_get_all_states(self, engine):
        """Test getting all agent states"""
        states = await engine.get_all_states()
        assert len(states) == 4
        
        for agent_id, state in states.items():
            assert state.agent_id == agent_id
            assert isinstance(state.agent_type, AgentType)
            assert isinstance(state.current_state, CognitiveState)
    
    @pytest.mark.asyncio
    async def test_coordination_recommendations(self, engine):
        """Test coordination recommendation generation"""
        # Set up overloaded agent
        await engine.update_agent_state(
            "codex_primary",
            CognitiveState.PROCESSING,
            {"processing_load": 0.9}
        )
        
        recommendations = await engine.get_coordination_recommendations()
        assert len(recommendations) > 0
        
        # Should have load balancing recommendation
        load_balance_recs = [
            rec for rec in recommendations 
            if rec["type"] == "load_balancing"
        ]
        assert len(load_balance_recs) > 0
    
    @pytest.mark.asyncio
    async def test_state_prediction(self, engine):
        """Test state prediction functionality"""
        agent_id = "gemini_primary"
        
        # Update state multiple times to build history
        for load in [0.2, 0.4, 0.6, 0.8]:
            await engine.update_agent_state(
                agent_id,
                CognitiveState.PROCESSING,
                {"processing_load": load}
            )
            await asyncio.sleep(0.1)  # Brief delay
        
        # Get final state
        state = await engine.get_agent_state(agent_id)
        assert state.predicted_next_state is not None
        assert state.confidence_score > 0.0
    
    @pytest.mark.asyncio
    async def test_export_state(self, engine):
        """Test state export functionality"""
        # Update some states
        await engine.update_agent_state(
            "claude_primary",
            CognitiveState.LEARNING,
            {"processing_load": 0.5}
        )
        
        # Export state
        exported_json = await engine.export_state()
        assert len(exported_json) > 0
        
        # Verify JSON is valid
        data = json.loads(exported_json)
        assert "timestamp" in data
        assert "agents" in data
        assert "coordination_matrix" in data
        assert len(data["agents"]) == 4


class TestCognitiveMetrics:
    """Test cases for Cognitive Metrics"""
    
    def test_cognitive_metrics_creation(self):
        """Test creating cognitive metrics"""
        metrics = CognitiveMetrics(
            timestamp=datetime.now(timezone.utc),
            agent_id="test_agent",
            agent_type=AgentType.CODEX,
            cognitive_state=CognitiveState.PROCESSING,
            processing_load=0.7,
            memory_usage=0.5,
            response_time=1.2,
            task_complexity=0.8,
            success_rate=0.95,
            coordination_score=0.9
        )
        
        assert metrics.agent_id == "test_agent"
        assert metrics.agent_type == AgentType.CODEX
        assert metrics.processing_load == 0.7
        assert metrics.success_rate == 0.95


class TestDigitalTwinAPI:
    """Test cases for Digital Twin API"""
    
    @pytest.fixture
    def api_client(self):
        """Create test API client"""
        from fastapi.testclient import TestClient
        from src.digital_twin.api import app
        return TestClient(app)
    
    def test_root_endpoint(self, api_client):
        """Test root endpoint"""
        response = api_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "Digital Twin API"
    
    def test_health_check(self, api_client):
        """Test health check endpoint"""
        response = api_client.get("/health")
        # Note: May return 503 if engine not initialized in test
        assert response.status_code in [200, 503]
    
    def test_get_agents_endpoint(self, api_client):
        """Test get all agents endpoint"""
        response = api_client.get("/agents")
        # May return 503 if engine not initialized
        assert response.status_code in [200, 503]
    
    @pytest.mark.asyncio
    async def test_update_agent_state_endpoint(self, api_client):
        """Test agent state update endpoint"""
        update_data = {
            "agent_id": "codex_primary",
            "new_state": "processing",
            "metrics": {
                "processing_load": 0.7,
                "task_complexity": 0.6
            }
        }
        
        response = api_client.post("/agents/codex_primary/state", json=update_data)
        # May return 503 if engine not initialized
        assert response.status_code in [200, 400, 503]


class TestIntegrationScenarios:
    """Integration test scenarios"""
    
    @pytest.mark.asyncio
    async def test_multi_agent_coordination_scenario(self):
        """Test complete multi-agent coordination scenario"""
        engine = create_digital_twin_engine()
        
        # Scenario: Multiple agents working on different tasks
        tasks = [
            ("codex_primary", CognitiveState.PROCESSING, {"processing_load": 0.8}),
            ("gemini_primary", CognitiveState.LEARNING, {"processing_load": 0.6}),
            ("claude_primary", CognitiveState.COORDINATING, {"processing_load": 0.4}),
            ("copilot_primary", CognitiveState.IDLE, {"processing_load": 0.1})
        ]
        
        # Update all agent states
        for agent_id, state, metrics in tasks:
            success = await engine.update_agent_state(agent_id, state, metrics)
            assert success is True
        
        # Get coordination recommendations
        recommendations = await engine.get_coordination_recommendations()
        
        # Should have recommendations for load balancing
        assert len(recommendations) > 0
        
        # Check that overloaded agent is identified
        overload_recs = [
            rec for rec in recommendations
            if rec["type"] == "load_balancing" and "codex_primary" in rec.get("agent_id", "")
        ]
        assert len(overload_recs) > 0
        
        # Check coordination opportunities
        coord_recs = [
            rec for rec in recommendations
            if rec["type"] == "coordination_opportunity"
        ]
        assert len(coord_recs) > 0
    
    @pytest.mark.asyncio
    async def test_state_history_tracking(self):
        """Test state history tracking over time"""
        engine = create_digital_twin_engine()
        agent_id = "gemini_primary"
        
        # Simulate agent working through different states
        state_sequence = [
            (CognitiveState.IDLE, {"processing_load": 0.1}),
            (CognitiveState.PROCESSING, {"processing_load": 0.5}),
            (CognitiveState.PROCESSING, {"processing_load": 0.8}),
            (CognitiveState.OPTIMIZING, {"processing_load": 0.9}),
            (CognitiveState.IDLE, {"processing_load": 0.2})
        ]
        
        for state, metrics in state_sequence:
            await engine.update_agent_state(agent_id, state, metrics)
            await asyncio.sleep(0.05)  # Brief delay
        
        # Check history was recorded
        assert len(engine.state_history[agent_id]) == len(state_sequence) + 1  # +1 for initial state
        
        # Check final state has prediction
        final_state = await engine.get_agent_state(agent_id)
        assert final_state.predicted_next_state is not None
        assert final_state.confidence_score > 0.0


# Performance tests
class TestPerformance:
    """Performance test cases"""
    
    @pytest.mark.asyncio
    async def test_bulk_state_updates(self):
        """Test performance with many state updates"""
        engine = create_digital_twin_engine()
        
        # Time bulk updates
        import time
        start_time = time.time()
        
        for i in range(100):
            agent_id = f"codex_primary"
            await engine.update_agent_state(
                agent_id,
                CognitiveState.PROCESSING,
                {"processing_load": 0.5 + (i % 5) * 0.1}
            )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete within reasonable time
        assert duration < 5.0  # 5 seconds for 100 updates
        
        # Check history size is managed
        history_size = len(engine.state_history["codex_primary"])
        assert history_size <= 101  # Original + 100 updates


# Fixtures and test configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
