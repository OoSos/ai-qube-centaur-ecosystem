"""
AI Qube Centaur System - Agent Integration Framework
CENTAUR-004: Multi-Agent Integration Module

This module provides the core framework for integrating and coordinating
multiple AI agents (Claude Pro, Gemini 2.5 Pro, OpenAI Codex, GitHub Copilot)
within the Centaur recursive learning system.

Author: GitHub Copilot (Node B) + Claude Pro (Node C)
Date: June 11, 2025
Task: CENTAUR-004 - Agent integration framework
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


class AgentCapability(Enum):
    """Enumeration of agent capabilities for task assignment optimization"""
    CODE_GENERATION = "code_generation"
    NATURAL_LANGUAGE = "natural_language"
    RESEARCH_ANALYSIS = "research_analysis"
    SYSTEM_ARCHITECTURE = "system_architecture"
    DATA_ANALYSIS = "data_analysis"
    CREATIVE_WRITING = "creative_writing"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"
    INTEGRATION = "integration"
    MONITORING = "monitoring"


class TaskPriority(Enum):
    """Task priority levels for agent coordination"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(Enum):
    """Task execution status tracking"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentMessage:
    """Standardized message format for inter-agent communication"""
    sender: str
    recipient: str
    task_id: str
    message_type: str
    priority: TaskPriority
    content: Dict[str, Any]
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "task_id": self.task_id,
            "message_type": self.message_type,
            "priority": self.priority.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMessage':
        """Create message from dictionary"""
        return cls(
            sender=data["sender"],
            recipient=data["recipient"],
            task_id=data["task_id"],
            message_type=data["message_type"],
            priority=TaskPriority(data["priority"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            correlation_id=data.get("correlation_id")
        )


@dataclass
class TaskDefinition:
    """Comprehensive task definition for agent assignment"""
    task_id: str
    title: str
    description: str
    required_capabilities: List[AgentCapability]
    priority: TaskPriority
    deadline: Optional[datetime]
    dependencies: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    deliverables: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.NOT_STARTED
    assigned_agents: List[str] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class BaseAgent(ABC):
    """Abstract base class for all AI agents in the Centaur system"""

    def __init__(self, agent_id: str, name: str,
                 capabilities: List[AgentCapability]):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = capabilities
        self.active_tasks: Dict[str, TaskDefinition] = {}
        self.message_queue: List[AgentMessage] = []
        self.is_available = True
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_response_time": 0.0,
            "last_active": datetime.now(timezone.utc)
        }

    @abstractmethod
    async def process_task(self, task: TaskDefinition) -> Dict[str, Any]:
        """Process a task and return results"""
        pass

    @abstractmethod
    async def handle_message(self, message: AgentMessage
                             ) -> Optional[AgentMessage]:
        """Handle incoming message and optionally return response"""
        pass

    def can_handle_task(self, task: TaskDefinition) -> bool:
        """Check if agent can handle the given task based on capabilities"""
        return any(cap in self.capabilities
                   for cap in task.required_capabilities)

    def get_workload(self) -> float:
        """Calculate current workload based on active tasks"""
        if not self.active_tasks:
            return 0.0

        total_weight = 0.0
        for task in self.active_tasks.values():
            weight = {
                TaskPriority.CRITICAL: 3.0,
                TaskPriority.HIGH: 2.0,
                TaskPriority.MEDIUM: 1.0,
                TaskPriority.LOW: 0.5
            }.get(task.priority, 1.0)
            total_weight += weight

        return total_weight

    def add_task(self, task: TaskDefinition) -> bool:
        """Add task to agent's active tasks"""
        if self.can_handle_task(task) and self.is_available:
            self.active_tasks[task.task_id] = task
            task.assigned_agents.append(self.agent_id)
            task.status = TaskStatus.IN_PROGRESS
            task.updated_at = datetime.now(timezone.utc)
            logger.info(f"Agent {self.name} assigned task {task.task_id}")
            return True
        return False

    def complete_task(self, task_id: str, results: Dict[str, Any]) -> bool:
        """Mark task as completed with results"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task.status = TaskStatus.COMPLETED
            task.updated_at = datetime.now(timezone.utc)
            task.context["results"] = results
            del self.active_tasks[task_id]
            self.performance_metrics["tasks_completed"] += 1
            logger.info(f"Agent {self.name} completed task {task_id}")
            return True
        return False

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "capabilities": [cap.value for cap in self.capabilities],
            "is_available": self.is_available,
            "active_tasks": len(self.active_tasks),
            "workload": self.get_workload(),
            "performance": self.performance_metrics,
            "last_seen": datetime.now(timezone.utc).isoformat()
        }


class AgentCoordinationFramework:
    """Central coordination framework for managing multiple AI agents"""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.tasks: Dict[str, TaskDefinition] = {}
        self.message_bus: List[AgentMessage] = []
        self.coordination_rules = {
            "max_concurrent_tasks_per_agent": 3,
            "task_timeout_hours": 24,
            "priority_preemption_enabled": True,
            "collaborative_task_support": True
        }
        logger.info("Agent Coordination Framework initialized")

    def register_agent(self, agent: BaseAgent) -> bool:
        """Register a new agent with the coordination framework"""
        if agent.agent_id not in self.agents:
            self.agents[agent.agent_id] = agent
            logger.info(f"Registered agent: {agent.name} ({agent.agent_id})")
            return True
        return False

    def create_task(self, task_def: TaskDefinition) -> bool:
        """Create and register a new task"""
        if task_def.task_id not in self.tasks:
            self.tasks[task_def.task_id] = task_def
            logger.info(f"Created task: {task_def.title} ({task_def.task_id})")
            return True
        return False

    def find_best_agent(self, task: TaskDefinition) -> Optional[str]:
        """Find the best agent for a given task based on capabilities"""
        suitable_agents = []

        for agent_id, agent in self.agents.items():
            if agent.can_handle_task(task) and agent.is_available:
                workload = agent.get_workload()
                max_tasks = self.coordination_rules["max_concurrent_tasks_per_agent"]
                if workload < max_tasks:
                    # Score based on capability match and current workload
                    cap_intersection = set(agent.capabilities) & set(task.required_capabilities)
                    capability_score = len(cap_intersection)
                    workload_score = 1.0 / (workload + 1.0)
                    total_score = capability_score * 2 + workload_score
                    suitable_agents.append((agent_id, total_score))

        if suitable_agents:
            # Return agent with highest score
            suitable_agents.sort(key=lambda x: x[1], reverse=True)
            return suitable_agents[0][0]

        return None

    async def assign_task(self, task_id: str,
                          agent_id: Optional[str] = None) -> bool:
        """Assign task to specific agent or find best available agent"""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return False

        task = self.tasks[task_id]

        if agent_id is None:
            agent_id = self.find_best_agent(task)

        if agent_id and agent_id in self.agents:
            agent = self.agents[agent_id]
            if agent.add_task(task):
                logger.info(f"Task {task_id} assigned to agent {agent.name}")
                # Notify agent of new task
                message = AgentMessage(
                    sender="coordination_framework",
                    recipient=agent_id,
                    task_id=task_id,
                    message_type="task_assignment",
                    priority=task.priority,
                    content={"task": task.__dict__}
                )
                await self.send_message(message)
                return True

        logger.warning(f"Could not assign task {task_id} to any agent")
        return False

    async def send_message(self, message: AgentMessage) -> bool:
        """Send message between agents through the coordination framework"""
        self.message_bus.append(message)

        if message.recipient in self.agents:
            recipient_agent = self.agents[message.recipient]
            recipient_agent.message_queue.append(message)
            logger.debug(f"Message sent from {message.sender} "
                        f"to {message.recipient}")
            return True

        logger.warning(f"Recipient {message.recipient} not found")
        return False

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status including all agents and tasks"""
        return {
            "framework_status": "operational",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agents": {agent_id: agent.get_status()
                      for agent_id, agent in self.agents.items()},
            "tasks": {
                "total": len(self.tasks),
                "not_started": len([t for t in self.tasks.values()
                                   if t.status == TaskStatus.NOT_STARTED]),
                "in_progress": len([t for t in self.tasks.values()
                                   if t.status == TaskStatus.IN_PROGRESS]),
                "completed": len([t for t in self.tasks.values()
                                 if t.status == TaskStatus.COMPLETED]),
                "blocked": len([t for t in self.tasks.values()
                               if t.status == TaskStatus.BLOCKED])
            },
            "message_queue_size": len(self.message_bus),
            "coordination_rules": self.coordination_rules
        }

    async def process_message_queue(self) -> None:
        """Process pending messages in the message bus"""
        messages_to_process = self.message_bus.copy()
        self.message_bus.clear()

        for message in messages_to_process:
            if message.recipient in self.agents:
                agent = self.agents[message.recipient]
                try:
                    response = await agent.handle_message(message)
                    if response:
                        await self.send_message(response)
                except Exception as e:
                    logger.error(f"Error processing message for "
                                f"{message.recipient}: {e}")


# Export main classes and enums for use by specific agent implementations
__all__ = [
    'BaseAgent',
    'AgentCoordinationFramework',
    'AgentMessage',
    'TaskDefinition',
    'AgentCapability',
    'TaskPriority',
    'TaskStatus'
]
