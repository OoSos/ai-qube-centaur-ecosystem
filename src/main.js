// AI Qube Centaur System - Main Application Entry Point
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'centaur-system',
        version: '1.0.0'
    });
});

// Basic status endpoint
app.get('/status', (req, res) => {
    res.json({
        message: 'AI Qube Centaur System is running',
        status: 'operational',
        services: {
            n8n: 'ready',
            agents: 'coordinating',
            database: 'connected'
        }
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🌟 AI Qube Centaur System started on port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
    console.log(`🔄 Status: http://localhost:${PORT}/status`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('🛑 Centaur System shutting down gracefully...');
    process.exit(0);
});

module.exports = app;
