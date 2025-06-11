-- PostgreSQL Schema for Centaur Multi-Agent Coordination Metrics
-- This schema supports the n8n workflow for tracking coordination performance

-- Create database if not exists
-- CREATE DATABASE centaur_coordination;

-- Main coordination metrics table
CREATE TABLE IF NOT EXISTS coordination_metrics (
    id SERIAL PRIMARY KEY,
    coordination_id VARCHAR(255) UNIQUE NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    selected_agent VARCHAR(50) NOT NULL,
    quality_score INTEGER CHECK (quality_score >= 0 AND quality_score <= 100),
    execution_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    routing_confidence DECIMAL(5,2),
    response_length INTEGER,
    success BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Agent performance tracking
CREATE TABLE IF NOT EXISTS agent_performance (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    task_type VARCHAR(100),
    total_tasks INTEGER DEFAULT 0,
    successful_tasks INTEGER DEFAULT 0,
    average_quality_score DECIMAL(5,2),
    average_response_time DECIMAL(8,2), -- in seconds
    current_load DECIMAL(3,2) DEFAULT 0.0,
    last_task_timestamp TIMESTAMP WITH TIME ZONE,
    performance_trend VARCHAR(20) DEFAULT 'stable', -- 'improving', 'declining', 'stable'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_name, task_type)
);

-- Task routing decisions log
CREATE TABLE IF NOT EXISTS routing_decisions (
    id SERIAL PRIMARY KEY,
    coordination_id VARCHAR(255) REFERENCES coordination_metrics(coordination_id),
    task_complexity VARCHAR(20),
    task_urgency VARCHAR(20),
    all_agent_scores JSONB, -- Store all agent scores for analysis
    routing_reason TEXT,
    decision_confidence DECIMAL(5,2),
    alternative_agents JSONB, -- Store other viable options
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- System performance aggregates (for dashboards)
CREATE TABLE IF NOT EXISTS system_performance_hourly (
    id SERIAL PRIMARY KEY,
    hour_timestamp TIMESTAMP WITH TIME ZONE,
    total_coordinations INTEGER DEFAULT 0,
    successful_coordinations INTEGER DEFAULT 0,
    average_quality_score DECIMAL(5,2),
    average_response_time DECIMAL(8,2),
    claude_usage_count INTEGER DEFAULT 0,
    codex_usage_count INTEGER DEFAULT 0,
    gemini_usage_count INTEGER DEFAULT 0,
    top_task_types JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(hour_timestamp)
);

-- Recursive learning patterns table
CREATE TABLE IF NOT EXISTS learning_patterns (
    id SERIAL PRIMARY KEY,
    pattern_type VARCHAR(100), -- 'successful_routing', 'quality_improvement', etc.
    task_type VARCHAR(100),
    pattern_data JSONB, -- Store the learned pattern
    confidence_level DECIMAL(5,2),
    usage_count INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2),
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_coordination_metrics_timestamp ON coordination_metrics(execution_time);
CREATE INDEX IF NOT EXISTS idx_coordination_metrics_agent ON coordination_metrics(selected_agent);
CREATE INDEX IF NOT EXISTS idx_coordination_metrics_task_type ON coordination_metrics(task_type);
CREATE INDEX IF NOT EXISTS idx_agent_performance_agent ON agent_performance(agent_name);
CREATE INDEX IF NOT EXISTS idx_routing_decisions_coordination ON routing_decisions(coordination_id);
CREATE INDEX IF NOT EXISTS idx_system_performance_hour ON system_performance_hourly(hour_timestamp);
CREATE INDEX IF NOT EXISTS idx_learning_patterns_type ON learning_patterns(pattern_type, task_type);

-- Views for common queries
CREATE OR REPLACE VIEW agent_performance_summary AS
SELECT 
    agent_name,
    SUM(total_tasks) as total_tasks,
    SUM(successful_tasks) as successful_tasks,
    ROUND(AVG(average_quality_score), 2) as avg_quality,
    ROUND(AVG(average_response_time), 2) as avg_response_time,
    ROUND(AVG(current_load), 3) as avg_load,
    MAX(last_task_timestamp) as last_active
FROM agent_performance 
GROUP BY agent_name;

CREATE OR REPLACE VIEW coordination_performance_daily AS
SELECT 
    DATE(execution_time) as date,
    COUNT(*) as total_coordinations,
    COUNT(*) FILTER (WHERE success = true) as successful_coordinations,
    ROUND(AVG(quality_score), 2) as avg_quality_score,
    selected_agent,
    task_type
FROM coordination_metrics 
WHERE execution_time >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(execution_time), selected_agent, task_type
ORDER BY date DESC;

-- Trigger to update agent performance stats
CREATE OR REPLACE FUNCTION update_agent_performance()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO agent_performance (agent_name, task_type, total_tasks, successful_tasks, average_quality_score)
    VALUES (NEW.selected_agent, NEW.task_type, 1, CASE WHEN NEW.success THEN 1 ELSE 0 END, NEW.quality_score)
    ON CONFLICT (agent_name, task_type) 
    DO UPDATE SET
        total_tasks = agent_performance.total_tasks + 1,
        successful_tasks = agent_performance.successful_tasks + CASE WHEN NEW.success THEN 1 ELSE 0 END,
        average_quality_score = (agent_performance.average_quality_score * agent_performance.total_tasks + NEW.quality_score) / (agent_performance.total_tasks + 1),
        last_task_timestamp = NEW.execution_time,
        updated_at = CURRENT_TIMESTAMP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_agent_performance
    AFTER INSERT ON coordination_metrics
    FOR EACH ROW
    EXECUTE FUNCTION update_agent_performance();

-- Initial agent configuration
INSERT INTO agent_performance (agent_name, task_type, average_quality_score, current_load) VALUES
('claude', 'analysis', 92.0, 0.3),
('claude', 'writing', 94.0, 0.3),
('claude', 'strategy', 90.0, 0.3),
('claude', 'research', 88.0, 0.3),
('codex', 'coding', 88.0, 0.4),
('codex', 'debugging', 85.0, 0.4),
('codex', 'architecture', 89.0, 0.4),
('codex', 'technical', 87.0, 0.4),
('gemini', 'multimodal', 85.0, 0.2),
('gemini', 'data_analysis', 83.0, 0.2),
('gemini', 'integration', 86.0, 0.2),
('gemini', 'optimization', 84.0, 0.2)
ON CONFLICT (agent_name, task_type) DO NOTHING;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO n8n_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO n8n_user;
