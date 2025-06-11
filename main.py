#!/usr/bin/env python3
"""
AI Qube Centaur System - Main Application Entry Point
Recursive Self-Improving Human-AI Collaboration Platform

This is the main entry point for the Centaur System, which orchestrates
the multi-agent coordination framework and recursive improvement engine.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.application import CentaurApplication
from src.core.config import Settings
from src.core.logger import setup_logging
from src.core.health import HealthChecker

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)


class CentaurSystemBootstrap:
    """Bootstrap class for the Centaur System"""
    
    def __init__(self):
        self.settings = Settings()
        self.app = None
        self.health_checker = HealthChecker()
        self._shutdown_event = asyncio.Event()
    
    async def startup(self):
        """Initialize and start the Centaur System"""
        try:
            logger.info("🚀 Starting AI Qube Centaur System")
            logger.info(f"Environment: {self.settings.environment}")
            logger.info(f"Debug Mode: {self.settings.debug}")
            
            # Perform health checks
            await self.health_checker.startup_checks()
            
            # Initialize the main application
            self.app = CentaurApplication(self.settings)
            await self.app.initialize()
            
            # Start the application
            await self.app.start()
            
            logger.info("✅ Centaur System startup complete")
            logger.info("🧠 Multi-agent coordination framework active")
            logger.info("🔄 Recursive improvement engine initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to start Centaur System: {e}")
            raise
    
    async def shutdown(self):
        """Gracefully shutdown the Centaur System"""
        try:
            logger.info("🛑 Shutting down Centaur System...")
            
            if self.app:
                await self.app.shutdown()
            
            logger.info("✅ Centaur System shutdown complete")
            
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")
            raise
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating shutdown...")
            self._shutdown_event.set()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def run(self):
        """Main run loop"""
        try:
            # Setup signal handlers
            self.setup_signal_handlers()
            
            # Start the system
            await self.startup()
            
            # Wait for shutdown signal
            await self._shutdown_event.wait()
            
            # Shutdown gracefully
            await self.shutdown()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            await self.shutdown()
        except Exception as e:
            logger.error(f"Fatal error in main loop: {e}")
            await self.shutdown()
            sys.exit(1)

async def main():
    """Main entry point"""
    try:
        # Print startup banner
        print_startup_banner()
        
        # Create and run the bootstrap
        bootstrap = CentaurSystemBootstrap()
        await bootstrap.run()
        
    except Exception as e:
        logger.error(f"Failed to start Centaur System: {e}")
        sys.exit(1)

def print_startup_banner():
    """Print the startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                  AI QUBE CENTAUR SYSTEM                     ║
    ║                                                              ║
    ║        Recursive Self-Improving Human-AI Collaboration      ║
    ║                         Platform                             ║
    ║                                                              ║
    ║  🧠 Multi-Agent Coordination Framework                      ║
    ║  🔄 Recursive Improvement Engine                            ║
    ║  🤖 Claude 4 + Codex + Gemini 2.5 Pro Integration         ║
    ║  🎯 Digital Twin Cognitive Modeling                        ║
    ║                                                              ║
    ║  Version: 0.1.0-alpha                                       ║
    ║  Status: Phase 1 Development                                ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

if __name__ == "__main__":
    # Set up asyncio event loop policy for Windows
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Run the main application
    asyncio.run(main())
