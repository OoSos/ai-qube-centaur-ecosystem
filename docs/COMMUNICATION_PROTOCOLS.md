# 🔄 CENTAUR-011: Multi-Agent Communication Protocols

**Date:** June 11, 2025  
**Assigned Agents:** Claude Pro (Primary) + GitHub Copilot (Technical Implementation)  
**Task ID:** CENTAUR-011  
**Priority:** High  
**Deadline:** June 16, 2025  

---

## 📋 **PROTOCOL OVERVIEW**

This document defines the standardized communication protocols for multi-agent coordination within the AI Qube Centaur System, enabling seamless collaboration between Claude Pro, Gemini 2.5 Pro, OpenAI Codex, and GitHub Copilot.

### **Design Goals:**
1. **Standardized Message Format**: Consistent structure across all agents
2. **Asynchronous Communication**: Non-blocking message passing
3. **Priority-Based Routing**: Critical messages get immediate attention
4. **Conflict Resolution**: Built-in mediation protocols
5. **Cross-Project Coordination**: Integration with Financial System TOM
6. **Scalable Architecture**: Support for additional agents

---

## 🔧 **CORE MESSAGE PROTOCOL**

### **Standard Message Format:**
```json
{
  "protocol_version": "1.0",
  "message_id": "unique_uuid",
  "timestamp": "2025-06-11T10:30:00Z",
  "sender": {
    "agent_id": "copilot | claude_pro | gemini_25_pro | codex",
    "node_id": "node_a | node_b | node_c | node_d",
    "system": "centaur | financial | both"
  },
  "recipient": {
    "agent_id": "copilot | claude_pro | gemini_25_pro | codex | all",
    "node_id": "node_a | node_b | node_c | node_d | broadcast",
    "system": "centaur | financial | both"
  },
  "message_type": "task_request | status_update | code_review | research_query | coordination | alert",
  "priority": "critical | high | medium | low",
  "context": {
    "task_id": "TASK-ID",
    "project": "centaur | financial",
    "dependencies": ["prerequisite_task_ids"],
    "deadline": "2025-06-16T17:00:00Z",
    "correlation_id": "conversation_thread_id"
  },
  "payload": {
    "content": "primary_message_content",
    "data": {},
    "attachments": ["file_paths"],
    "required_response": true,
    "response_deadline": "2025-06-11T12:00:00Z"
  },
  "routing": {
    "delivery_method": "direct | broadcast | queue",
    "retry_count": 0,
    "max_retries": 3,
    "fallback_recipients": ["backup_agent_ids"]
  }
}
```

---

## 🎯 **MESSAGE TYPES & WORKFLOWS**

### **1. Task Assignment Protocol**
```json
{
  "message_type": "task_request",
  "priority": "high",
  "payload": {
    "content": "Agent assignment request for CENTAUR-012",
    "data": {
      "task_definition": {
        "task_id": "CENTAUR-012",
        "title": "Digital Twin Cognitive Core",
        "description": "Implement cognitive state modeling",
        "required_capabilities": ["code_generation", "system_architecture"],
        "estimated_effort": "8 hours",
        "deliverables": ["core_module", "tests", "documentation"]
      }
    },
    "required_response": true,
    "response_deadline": "2025-06-11T11:00:00Z"
  }
}
```

**Response Format:**
```json
{
  "message_type": "task_response",
  "payload": {
    "content": "Task acceptance/rejection",
    "data": {
      "status": "accepted | rejected | requires_negotiation",
      "availability": "2025-06-11T14:00:00Z",
      "estimated_completion": "2025-06-16T17:00:00Z",
      "conditions": ["dependency_requirements"],
      "alternative_agents": ["suggested_alternatives"]
    }
  }
}
```

### **2. Status Update Protocol**
```json
{
  "message_type": "status_update",
  "priority": "medium",
  "payload": {
    "content": "Task progress update",
    "data": {
      "task_id": "CENTAUR-012",
      "progress_percentage": 65,
      "status": "in_progress | blocked | completed",
      "blockers": ["dependency_issues"],
      "next_milestone": "core_implementation_complete",
      "eta": "2025-06-15T16:00:00Z"
    }
  }
}
```

### **3. Code Review Protocol**
```json
{
  "message_type": "code_review",
  "priority": "medium",
  "payload": {
    "content": "Code review request for digital twin module",
    "data": {
      "repository": "centaur-development",
      "branch": "feature/digital-twin-core",
      "files": ["src/digital_twin/cognitive_core.py"],
      "review_type": "security | performance | architecture | style",
      "review_deadline": "2025-06-12T10:00:00Z"
    },
    "attachments": ["code_diff.patch"]
  }
}
```

### **4. Research Query Protocol**
```json
{
  "message_type": "research_query",
  "priority": "medium",
  "payload": {
    "content": "Research request: optimal vector database for RAG",
    "data": {
      "research_topic": "vector_database_comparison",
      "scope": "technical_specifications",
      "use_case": "RAG_integration_centaur_system",
      "requirements": ["scalability", "performance", "python_integration"],
      "deliverable_format": "comparison_report"
    }
  }
}
```

### **5. Coordination Protocol**
```json
{
  "message_type": "coordination",
  "priority": "high",
  "payload": {
    "content": "Cross-project coordination request",
    "data": {
      "coordination_type": "resource_conflict | priority_alignment | dependency_resolution",
      "affected_tasks": ["CENTAUR-013", "FINANCIAL-002"],
      "proposed_solution": "schedule_adjustment",
      "impact_assessment": "minimal_delay_acceptable"
    }
  }
}
```

---

## 🚨 **ALERT & ESCALATION PROTOCOLS**

### **Critical Alert Format:**
```json
{
  "message_type": "alert",
  "priority": "critical",
  "payload": {
    "content": "System performance degradation detected",
    "data": {
      "alert_type": "performance | security | dependency | failure",
      "affected_systems": ["financial_deployment"],
      "severity": "critical | high | medium | low",
      "required_action": "immediate_attention | investigation | monitoring",
      "escalation_path": ["vs_code_coordinator", "human_oversight"]
    }
  }
}
```

### **Escalation Procedures:**
1. **Level 1 - Agent-to-Agent**: Direct communication (response within 1 hour)
2. **Level 2 - Coordination Framework**: Automated mediation (response within 4 hours)
3. **Level 3 - VS Code Coordinator**: Cross-project impacts (response within 8 hours)
4. **Level 4 - Human Oversight**: Strategic conflicts (response within 24 hours)

---

## 🔄 **ROUTING & DELIVERY MECHANISMS**

### **1. Direct Messaging**
- **Use Case**: Specific agent-to-agent communication
- **Delivery**: Immediate push to recipient's message queue
- **Reliability**: Guaranteed delivery with acknowledgment
- **Examples**: Task assignments, code reviews, specific queries

### **2. Broadcast Messaging**
- **Use Case**: System-wide announcements, status updates
- **Delivery**: Push to all registered agents
- **Reliability**: Best-effort delivery
- **Examples**: System alerts, coordination updates, milestone announcements

### **3. Queue-Based Messaging**
- **Use Case**: Non-urgent communication, batch processing
- **Delivery**: Added to processing queue, handled in order
- **Reliability**: Persistent storage with retry logic
- **Examples**: Research requests, documentation updates, non-critical updates

### **4. Priority Routing**
```
Critical:   Immediate delivery, bypass queue
High:       Priority queue, <1 hour delivery
Medium:     Standard queue, <4 hour delivery  
Low:        Background queue, <24 hour delivery
```

---

## 🛡️ **CONFLICT RESOLUTION PROTOCOLS**

### **Resource Conflict Resolution:**
1. **Detection**: Automated workload monitoring
2. **Assessment**: Priority-based task evaluation
3. **Mediation**: Coordination framework arbitration
4. **Resolution**: Task reassignment or scheduling adjustment
5. **Monitoring**: Ongoing conflict prevention

### **Priority Conflict Matrix:**
```
Financial System Tasks > Centaur Critical Tasks > Centaur High Tasks > Others
```

### **Conflict Resolution Message:**
```json
{
  "message_type": "coordination",
  "priority": "high",
  "payload": {
    "content": "Resource conflict resolution",
    "data": {
      "conflict_type": "agent_overload | priority_clash | dependency_cycle",
      "affected_agents": ["copilot", "claude_pro"],
      "proposed_resolution": "task_reassignment | schedule_adjustment | resource_scaling",
      "timeline": "immediate | within_4_hours | next_business_day"
    }
  }
}
```

---

## 📊 **MONITORING & ANALYTICS**

### **Message Flow Metrics:**
- **Delivery Rate**: Percentage of messages successfully delivered
- **Response Time**: Average time from send to acknowledgment
- **Queue Depth**: Number of pending messages per agent
- **Error Rate**: Failed delivery attempts and causes

### **Agent Performance Metrics:**
- **Availability**: Agent online/offline status tracking
- **Workload**: Current task count and priority distribution
- **Response Time**: Average time to respond to messages
- **Task Completion Rate**: Success rate for assigned tasks

### **System Health Indicators:**
- **Message Throughput**: Messages processed per hour
- **Conflict Rate**: Number of conflicts detected and resolved
- **Escalation Rate**: Messages requiring higher-level intervention
- **Cross-Project Coordination Efficiency**: Financial vs Centaur task balance

---

## 🔧 **TECHNICAL IMPLEMENTATION**

### **Message Bus Architecture:**
```python
class MessageBus:
    def __init__(self):
        self.message_queue = asyncio.Queue()
        self.agents = {}
        self.routing_table = {}
        self.message_history = []
    
    async def send_message(self, message: AgentMessage):
        # Validate message format
        # Route based on priority and recipient
        # Store for audit trail
        # Deliver with retry logic
    
    async def process_messages(self):
        # Background message processing
        # Priority-based delivery
        # Error handling and retries
```

### **Protocol Validation:**
```python
def validate_message(message: dict) -> bool:
    required_fields = ['protocol_version', 'sender', 'recipient', 'message_type']
    return all(field in message for field in required_fields)
```

---

## ✅ **PROTOCOL TESTING & VALIDATION**

### **Test Scenarios:**
1. **Basic Message Delivery**: Send/receive between all agent pairs
2. **Priority Handling**: Critical messages bypass queue
3. **Broadcast Distribution**: System-wide announcements
4. **Conflict Resolution**: Simulated resource conflicts
5. **Cross-Project Coordination**: Financial/Centaur integration
6. **Error Handling**: Network failures, agent unavailability
7. **Performance Load Testing**: High message volume handling

### **Validation Checklist:**
- [ ] Message format compliance
- [ ] Priority-based routing
- [ ] Reliable delivery guarantees
- [ ] Conflict detection and resolution
- [ ] Cross-project coordination
- [ ] Performance requirements met
- [ ] Security and validation checks
- [ ] Monitoring and analytics functional

---

## 🚀 **DEPLOYMENT & INTEGRATION**

### **Phase 1: Core Protocol Implementation**
- [x] Message format standardization
- [x] Basic routing mechanisms
- [ ] Agent integration with protocol
- [ ] Testing and validation

### **Phase 2: Advanced Features**
- [ ] Conflict resolution automation
- [ ] Cross-project coordination
- [ ] Performance optimization
- [ ] Monitoring dashboard

### **Phase 3: Production Deployment**
- [ ] Integration with existing TOM framework
- [ ] Financial System coordination
- [ ] Full monitoring and alerting
- [ ] Documentation and training

---

## 📝 **PROTOCOL GOVERNANCE**

### **Change Management:**
- **Minor Updates**: Agent-level implementation changes
- **Major Updates**: Protocol version changes requiring all agents
- **Emergency Changes**: Critical security or performance fixes

### **Version Control:**
- **Current Version**: 1.0
- **Backward Compatibility**: Support previous version for 30 days
- **Upgrade Path**: Automated migration tools provided

---

**✅ CENTAUR-011: Multi-Agent Communication Protocols - FRAMEWORK COMPLETE**

*This protocol framework enables coordinated execution of all Centaur System development tasks while maintaining integration with the operational Financial System.*

---

_Designed by Claude Pro (Node C) + GitHub Copilot (Node B)_  
_Date: June 11, 2025_  
_Next Review: June 18, 2025_
