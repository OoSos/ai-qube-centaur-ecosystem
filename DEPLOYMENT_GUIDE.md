# 🚀 AI Qube Centaur Ecosystem - Deployment Guide

**Version:** 2.0.0  
**Date:** June 11, 2025  
**Status:** Production Ready - 95% Deployment Complete  

---

## 📋 **Pre-Deployment Checklist**

### **Required Environment Variables**

```bash
# AI Service API Keys
export ANTHROPIC_API_KEY="your_claude_api_key"      # Required for agent coordination
export OPENAI_API_KEY="your_openai_api_key"         # Required for digital twin
export GOOGLE_API_KEY="your_gemini_api_key"         # Required for RAG system

# Database Configuration
export POSTGRES_PASSWORD="your_db_password"         # Required for coordination metrics
export POSTGRES_USER="centaur_admin"                # Optional (defaults to postgres)
export POSTGRES_DB="centaur_coordination"           # Optional (defaults to centaur)

# Integration Services
export GITHUB_TOKEN="your_github_token"             # Required for webhook integration
export WEAVIATE_URL="http://localhost:8080"         # Optional (defaults to localhost)
export N8N_URL="http://localhost:5678"              # Optional (defaults to localhost)
```

### **System Requirements**

```yaml
Minimum:
  OS: Windows 10/11, macOS 12+, Ubuntu 20.04+
  Python: 3.8+
  RAM: 8GB
  Storage: 5GB free space
  Network: Stable internet connection

Recommended:
  OS: Windows 11, macOS 14+, Ubuntu 22.04+
  Python: 3.11+
  RAM: 16GB+
  Storage: 20GB+ SSD
  Network: High-speed internet (100Mbps+)
```

---

## 🛠️ **Installation Steps**

### **1. Repository Setup**

```bash
# Clone the repository
git clone https://github.com/OoSos/ai-qube-centaur-ecosystem.git
cd ai-qube-centaur-ecosystem

# Verify all files are present
ls -la
# Expected: README.md, requirements.txt, src/, scripts/, n8n-workflows/, etc.
```

### **2. Python Environment Setup**

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
python -c "import openai, anthropic, google.generativeai, weaviate, psycopg2; print('All dependencies installed successfully')"
```

### **3. Database Setup**

```bash
# Start PostgreSQL service
# Windows: net start postgresql
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database
createdb centaur_coordination

# Deploy schema
psql -U postgres -d centaur_coordination < database/coordination_schema.sql

# Verify database setup
psql -U postgres -d centaur_coordination -c "\dt"
# Expected: Tables for agent_metrics, task_history, coordination_logs, etc.
```

### **4. Vector Database Setup (Weaviate)**

```bash
# Using Docker (Recommended)
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  semitechnologies/weaviate:latest

# Verify Weaviate is running
curl http://localhost:8080/v1/.well-known/ready
# Expected: {"status": "ok"}

# Alternative: Using Docker Compose
docker-compose up -d weaviate
```

### **5. n8n Workflow Platform Setup**

```bash
# Install n8n globally
npm install -g n8n

# Start n8n with tunnel for webhook access
n8n start --tunnel

# Alternative: Using Docker
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e WEBHOOK_URL=http://localhost:5678 \
  n8nio/n8n

# Verify n8n is accessible
curl http://localhost:5678/healthz
# Expected: {"status": "ok"}
```

---

## 🚀 **Deployment Execution**

### **Phase 1: Core System Deployment**

```bash
# Set environment variables
export ANTHROPIC_API_KEY="your_claude_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export GOOGLE_API_KEY="your_gemini_api_key"
export POSTGRES_PASSWORD="your_db_password"

# Deploy n8n workflows
python scripts/deploy_n8n_workflows.py

# Expected output:
# ✅ PostgreSQL connection established
# ✅ n8n workflows deployed successfully
# ✅ Webhook endpoints configured
# ✅ Agent coordination active
```

### **Phase 2: Knowledge Base Population**

```bash
# Populate RAG system with knowledge base
python scripts/populate_rag_system.py

# Expected output:
# ✅ Weaviate connection established
# ✅ Schema created successfully
# ✅ Documentation indexed (X documents)
# ✅ Agent capabilities mapped
# ✅ RAG system operational
```

### **Phase 3: Integration Testing**

```bash
# Test end-to-end integration pipeline
export GITHUB_TOKEN="your_github_token"
python scripts/end_to_end_integration.py

# Expected output:
# ✅ GitHub webhook configured
# ✅ Integration workflow created
# ✅ End-to-end pipeline tested (3/3 tests passing)
# ✅ Performance dashboard generated
```

---

## 📊 **Verification & Monitoring**

### **Health Checks**

```bash
# Check all services status
python scripts/health_check.py

# Expected output:
# ✅ PostgreSQL: Connected
# ✅ Weaviate: Operational
# ✅ n8n: Active workflows (2)
# ✅ AI Services: All APIs responding
# ✅ GitHub Integration: Webhook active
```

### **Performance Dashboard**

```bash
# Generate and open performance dashboard
python scripts/generate_dashboard.py

# Dashboard will be available at:
# file://dashboard/coordination_dashboard.html
```

### **Real-Time Monitoring**

Access monitoring endpoints:
- **System Health**: `http://localhost:8000/health`
- **Agent Status**: `http://localhost:8000/api/v1/agents/status`
- **Performance Metrics**: `http://localhost:8000/api/v1/metrics`
- **n8n Workflows**: `http://localhost:5678/workflows`

---

## 🔧 **Configuration Management**

### **Environment Configuration**

Create `.env` file in project root:
```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
nano .env  # or your preferred editor
```

Example `.env` file:
```bash
# AI Service Configuration
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_gemini_api_key

# Database Configuration
POSTGRES_URL=postgresql://postgres:password@localhost:5432/centaur_coordination
POSTGRES_PASSWORD=your_secure_password

# Service URLs
WEAVIATE_URL=http://localhost:8080
N8N_URL=http://localhost:5678

# GitHub Integration
GITHUB_TOKEN=your_github_token
GITHUB_WEBHOOK_SECRET=your_webhook_secret

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### **Advanced Configuration**

```yaml
# config/production.yaml
agents:
  claude:
    model: "claude-3-opus-20240229"
    max_tokens: 4096
    temperature: 0.1
  
  openai:
    model: "gpt-4-turbo-preview"
    max_tokens: 4096
    temperature: 0.1
  
  gemini:
    model: "gemini-2.5-pro"
    max_tokens: 4096
    temperature: 0.1

coordination:
  max_concurrent_tasks: 10
  task_timeout: 300
  retry_attempts: 3
  
monitoring:
  metrics_retention: "30d"
  alert_thresholds:
    response_time: 2000  # milliseconds
    error_rate: 0.05     # 5%
    success_rate: 0.95   # 95%
```

---

## 🐳 **Docker Deployment (Production)**

### **Using Docker Compose**

```bash
# Production deployment with Docker
docker-compose -f docker-compose.prod.yml up -d

# Scale services as needed
docker-compose scale agents=3 workers=5

# View logs
docker-compose logs -f centaur-coordinator

# Stop services
docker-compose down
```

### **Docker Compose Configuration**

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: centaur_coordination
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/coordination_schema.sql:/docker-entrypoint-initdb.d/schema.sql
    ports:
      - "5432:5432"

  weaviate:
    image: semitechnologies/weaviate:latest
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: true
    ports:
      - "8080:8080"

  n8n:
    image: n8nio/n8n
    environment:
      N8N_BASIC_AUTH_ACTIVE: true
      N8N_BASIC_AUTH_USER: admin
      N8N_BASIC_AUTH_PASSWORD: ${N8N_PASSWORD}
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n

  centaur-coordinator:
    build: .
    environment:
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}
      POSTGRES_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/centaur_coordination
    depends_on:
      - postgres
      - weaviate
      - n8n
    ports:
      - "8000:8000"

volumes:
  postgres_data:
  n8n_data:
```

---

## 🔍 **Troubleshooting**

### **Common Issues**

#### **API Key Authentication Errors**
```bash
# Verify API keys are set
echo $ANTHROPIC_API_KEY | head -c 20
echo $OPENAI_API_KEY | head -c 20
echo $GOOGLE_API_KEY | head -c 20

# Test API connectivity
python -c "
import openai
client = openai.OpenAI()
response = client.models.list()
print('OpenAI API: Connected')
"
```

#### **Database Connection Issues**
```bash
# Check PostgreSQL status
pg_isready -h localhost -p 5432

# Test database connection
psql -U postgres -d centaur_coordination -c "SELECT 1;"

# Reset database if needed
dropdb centaur_coordination
createdb centaur_coordination
psql -U postgres -d centaur_coordination < database/coordination_schema.sql
```

#### **Service Port Conflicts**
```bash
# Check what's using ports
netstat -tulpn | grep :5678  # n8n
netstat -tulpn | grep :8080  # Weaviate
netstat -tulpn | grep :5432  # PostgreSQL

# Kill conflicting processes if needed
sudo kill $(sudo lsof -t -i:5678)
```

### **Performance Optimization**

#### **Database Tuning**
```sql
-- PostgreSQL optimization
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET max_connections = '200';
ALTER SYSTEM SET work_mem = '4MB';
SELECT pg_reload_conf();
```

#### **Memory Management**
```bash
# Monitor memory usage
top -p $(pgrep -f "centaur")

# Adjust Python memory limits
export PYTHONMALLOC=malloc
export MALLOC_ARENA_MAX=2
```

---

## 📈 **Production Monitoring**

### **Metrics Collection**

```bash
# Start Prometheus monitoring
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Start Grafana dashboard
docker run -d \
  --name grafana \
  -p 3000:3000 \
  grafana/grafana
```

### **Alert Configuration**

```yaml
# monitoring/alerts.yml
groups:
  - name: centaur_alerts
    rules:
      - alert: HighResponseTime
        expr: avg_response_time > 2000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"

      - alert: LowSuccessRate
        expr: success_rate < 0.95
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Success rate below threshold"
```

---

## 🔐 **Security Considerations**

### **API Key Management**
- Store API keys in secure environment variables
- Use secrets management systems in production
- Rotate keys regularly (quarterly)
- Monitor API usage for anomalies

### **Network Security**
- Use HTTPS for all external communications
- Implement rate limiting on API endpoints
- Set up firewall rules for service ports
- Enable VPN access for production environments

### **Database Security**
- Use strong passwords for database users
- Enable SSL connections for PostgreSQL
- Implement database user access controls
- Regular security updates and backups

---

## 📚 **Additional Resources**

### **Documentation**
- [Agent Integration Guide](docs/agent_integration.md)
- [Digital Twin API Reference](docs/digital_twin_api.md)
- [RAG System Configuration](docs/rag_configuration.md)
- [n8n Workflow Development](docs/n8n_workflows.md)

### **Support**
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Community support and questions
- **Documentation Wiki**: Comprehensive guides and tutorials

### **Community**
- **Discord**: Real-time community chat
- **GitHub Discussions**: Technical discussions
- **Blog**: Latest updates and use cases

---

## ✅ **Deployment Completion Checklist**

- [ ] Environment variables configured
- [ ] Dependencies installed successfully
- [ ] PostgreSQL database deployed and tested
- [ ] Weaviate vector database operational
- [ ] n8n workflows imported and active
- [ ] All deployment scripts executed successfully
- [ ] Health checks passing
- [ ] Performance dashboard accessible
- [ ] Integration tests completed
- [ ] Monitoring alerts configured
- [ ] Documentation reviewed
- [ ] Security measures implemented

---

**🎉 Congratulations! Your AI Qube Centaur Ecosystem is now fully deployed and operational.**

*Ready for production workloads and market demonstration.*
