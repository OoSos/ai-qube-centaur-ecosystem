# Multi-stage Dockerfile for Centaur System
FROM node:18-alpine AS node-base

# Install Python and build dependencies
RUN apk add --no-cache python3 py3-pip build-base postgresql-dev

# Create Python virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create app directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY requirements.txt ./

# Install Node.js dependencies
RUN npm ci --only=production

# Install Python dependencies in virtual environment
RUN source /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data models

# Set permissions
RUN chown -R node:node /app
USER node

# Expose ports
EXPOSE 8000 5678

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["npm", "start"]
