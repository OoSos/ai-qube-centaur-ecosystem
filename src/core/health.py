"""
Health checking system for the Centaur System
"""

import asyncio
import logging
from typing import Dict, List, Optional
import httpx
import redis
import psycopg2
from src.core.config import Settings

logger = logging.getLogger("centaur.health")


class HealthChecker:
    """System health monitoring and startup checks"""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.health_status = {}
    
    async def startup_checks(self) -> bool:
        """Perform comprehensive startup health checks"""
        logger.info("🏥 Performing startup health checks...")
        
        checks = [
            ("database", self._check_database),
            ("redis", self._check_redis),
            ("n8n", self._check_n8n),
            ("ai_apis", self._check_ai_apis),
        ]
        
        all_healthy = True
        
        for check_name, check_func in checks:
            try:
                result = await check_func()
                self.health_status[check_name] = {
                    "status": "healthy" if result else "unhealthy",
                    "timestamp": asyncio.get_event_loop().time()
                }
                
                if result:
                    logger.info(f"✅ {check_name.upper()} health check passed")
                else:
                    logger.error(f"❌ {check_name.upper()} health check failed")
                    all_healthy = False
                    
            except Exception as e:
                logger.error(f"❌ {check_name.upper()} health check error: {e}")
                self.health_status[check_name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": asyncio.get_event_loop().time()
                }
                all_healthy = False
        
        if all_healthy:
            logger.info("🎉 All startup health checks passed!")
        else:
            logger.warning("⚠️ Some health checks failed - check logs for details")
        
        return all_healthy
    
    async def _check_database(self) -> bool:
        """Check PostgreSQL database connectivity"""
        try:
            # Extract connection parameters from DATABASE_URL
            conn = psycopg2.connect(self.settings.database_url)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    async def _check_redis(self) -> bool:
        """Check Redis connectivity"""
        try:
            r = redis.from_url(self.settings.redis_url)
            r.ping()
            r.close()
            return True
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            return False
    
    async def _check_n8n(self) -> bool:
        """Check n8n service availability"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.settings.n8n_base_url}/healthz",
                    timeout=5.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.warning(f"n8n health check failed: {e}")
            # n8n might not be started yet, so this is a warning not error
            return False
    
    async def _check_ai_apis(self) -> bool:
        """Check AI API connectivity"""
        # For startup, we just verify the API keys are configured
        # Full API checks will be done when agents are initialized
        required_keys = [
            self.settings.anthropic_api_key,
            self.settings.openai_api_key,
            self.settings.google_ai_api_key
        ]
        
        if all(key and len(key) > 10 for key in required_keys):
            logger.info("🔑 AI API keys configured")
            return True
        else:
            logger.error("🔑 Missing or invalid AI API keys")
            return False
    
    async def get_health_status(self) -> Dict:
        """Get current health status"""
        return {
            "status": "healthy" if all(
                check.get("status") == "healthy" 
                for check in self.health_status.values()
            ) else "unhealthy",
            "checks": self.health_status,
            "timestamp": asyncio.get_event_loop().time()
        }
    
    async def periodic_health_check(self, interval: int = 30):
        """Run periodic health checks"""
        while True:
            try:
                await asyncio.sleep(interval)
                await self.startup_checks()
            except Exception as e:
                logger.error(f"Periodic health check error: {e}")
                await asyncio.sleep(interval)
