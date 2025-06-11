# 🖥️ Centaur Control Center - Desktop GUI

A simple, professional desktop application for managing the AI Qube Centaur Ecosystem with one-click deployment and monitoring.

## 🚀 Quick Start

### **Method 1: Double-Click Launch (Easiest)**
1. Double-click `Launch_Centaur.bat` 
2. The GUI will open automatically

### **Method 2: Create Desktop Shortcut**
1. Double-click `Create_Desktop_Shortcut.bat`
2. A shortcut will appear on your desktop
3. Double-click the desktop shortcut to launch

### **Method 3: Command Line**
```bash
python centaur_launcher.py
```

## 🎯 Features

### **🔍 Real-Time Status Monitoring**
- PostgreSQL Database status
- Weaviate Vector Database status  
- n8n Workflow Engine status
- AI Service API connectivity

### **⚡ One-Click Operations**
- **🚀 Deploy Centaur System** - Full system deployment
- **⚙️ Configure Environment** - Set API keys and configuration
- **🗄️ Setup Database** - Initialize PostgreSQL database
- **🧠 Deploy AI Services** - Configure AI integrations
- **📊 Open Dashboard** - View performance monitoring
- **🔍 Health Check** - Comprehensive system validation

### **📋 System Management**
- Real-time log monitoring
- Service start/stop controls
- Configuration management
- Performance monitoring

## 📋 Prerequisites

### **Required:**
- Windows 10/11 (GUI optimized for Windows)
- Python 3.8+ installed
- Internet connection for API services

### **API Keys Needed:**
- `ANTHROPIC_API_KEY` - Claude AI API
- `OPENAI_API_KEY` - OpenAI API  
- `GOOGLE_API_KEY` - Google Gemini API
- `POSTGRES_PASSWORD` - Database password

### **Optional Services:**
- PostgreSQL (can be installed via Docker)
- Weaviate Vector Database (can be installed via Docker)
- n8n Workflow Engine (can be installed via npm)

## 🛠️ Setup Instructions

### **1. Environment Setup**
Click "⚙️ Configure Environment" in the GUI to set your API keys:

```bash
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key  
GOOGLE_API_KEY=your_gemini_api_key
POSTGRES_PASSWORD=your_secure_password
GITHUB_TOKEN=your_github_token (optional)
```

### **2. Install Dependencies**
The GUI will check dependencies automatically. If missing:
```bash
pip install -r requirements.txt
```

### **3. Start Services** 
Use the GUI buttons or manual setup:

**PostgreSQL:**
```bash
# Using Docker (Recommended)
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=your_password postgres:15
```

**Weaviate:**
```bash
# Using Docker
docker run -d --name weaviate -p 8080:8080 semitechnologies/weaviate:latest
```

**n8n:**
```bash
# Using npm
npm install -g n8n
n8n start
```

### **4. Deploy System**
1. Click "🚀 DEPLOY CENTAUR SYSTEM"
2. Monitor progress in the log panel
3. System will automatically configure all components

## 📊 GUI Interface Overview

```
🏛️ AI Qube Centaur Ecosystem - Control Center
┌─────────────────────────────────────────────────────┐
│ 🔍 System Status                                   │
│ PostgreSQL Database:     🟢 Online                 │
│ Weaviate Vector DB:      🔴 Offline                │
│ n8n Workflow Engine:     🟢 Online                 │  
│ AI Service APIs:         🟡 Partial                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🚀 Control Center                                  │
│                                                     │
│        🚀 DEPLOY CENTAUR SYSTEM                    │
│                                                     │
│ ⚙️ Configure Environment  🗄️ Setup Database       │
│ 🧠 Deploy AI Services     📊 Open Dashboard        │
│ 🔍 Health Check          📋 View Logs             │
│ ⏹️ Stop Services         🔄 Restart System        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 📋 System Logs                                     │
│                                                     │
│ [2025-06-11 07:30:00] 🏛️ Control Center Started   │
│ [2025-06-11 07:30:05] 📊 Status: 95% Ready        │
│ [2025-06-11 07:30:10] ⚡ Environment configured    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🔧 Troubleshooting

### **Common Issues:**

**❌ "Python not found"**
- Install Python 3.8+ from python.org
- Add Python to your PATH

**❌ "tkinter not available"** 
- On Windows: Usually included with Python
- On Linux: `sudo apt-get install python3-tk`

**❌ "Service connection failed"**
- Check if services are running
- Verify firewall settings
- Ensure correct ports are available

**❌ "API key authentication failed"**
- Verify API keys are correctly set
- Check API key permissions and quotas
- Ensure internet connectivity

### **Service Status Indicators:**
- 🟢 **Online** - Service running and accessible
- 🔴 **Offline** - Service not running or unreachable
- 🟡 **Partial** - Some components available

### **Reset Instructions:**
1. Click "⏹️ Stop Services"
2. Wait 10 seconds
3. Click "🔄 Restart System"
4. Monitor logs for startup progress

## 📈 Performance Monitoring

The GUI provides real-time monitoring through:

- **Status Panel** - Service availability
- **Log Panel** - Real-time system messages  
- **Dashboard Button** - Opens web-based performance dashboard
- **Health Check** - Comprehensive system validation

## 🔐 Security Notes

- API keys are stored in environment variables (secure)
- Database passwords are not logged or displayed
- All communications use secure protocols
- Local services use standard ports with firewall protection

## 📚 Additional Resources

- **Main Documentation**: `README.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`  
- **Health Check**: Click "🔍 Health Check" in GUI
- **Performance Dashboard**: Click "📊 Open Dashboard" in GUI

## 🎯 Quick Reference

| Button | Function | Description |
|--------|----------|-------------|
| 🚀 | Deploy System | Full automated deployment |
| ⚙️ | Configure Env | Set API keys and config |
| 🗄️ | Setup Database | Initialize PostgreSQL |
| 🧠 | Deploy AI | Configure AI services |
| 📊 | Open Dashboard | Performance monitoring |
| 🔍 | Health Check | System validation |
| 📋 | View Logs | Detailed log viewer |
| ⏹️ | Stop Services | Graceful shutdown |
| 🔄 | Restart | Full system restart |

---

**🎉 Ready to revolutionize AI coordination with a simple click!**

*Professional desktop interface for enterprise-grade AI orchestration*
