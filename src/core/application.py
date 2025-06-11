"""
Main Centaur System Application
"""

import asyncio
import logging
from typing import Optional

from src.core.config import Settings
from src.core.logger import get_logger
from src.coordination.orchestrator import CentaurOrchestrator
from src.agents.manager import AgentManager
from src.recursive_engine.engine import RecursiveImprovementEngine
from src.digital_twin.twin import DigitalTwinManager

logger = get_logger("application")


class CentaurApplication:
    """Main application class for the Centaur System"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.orchestrator: Optional[CentaurOrchestrator] = None
        self.agent_manager: Optional[AgentManager] = None
        self.recursive_engine: Optional[RecursiveImprovementEngine] = None
        self.digital_twin_manager: Optional[DigitalTwinManager] = None
        self._running = False
    
    async def initialize(self):
        """Initialize all system components"""
        logger.info("🚀 Initializing Centaur System components...")
        
        try:
            # Initialize Digital Twin Manager
            logger.info("🧠 Initializing Digital Twin Manager...")
            self.digital_twin_manager = DigitalTwinManager(self.settings)
            await self.digital_twin_manager.initialize()
            
            # Initialize Agent Manager
            logger.info("🤖 Initializing AI Agent Manager...")
            self.agent_manager = AgentManager(self.settings)
            await self.agent_manager.initialize()
            
            # Initialize Orchestrator
            logger.info("🎼 Initializing Centaur Orchestrator...")
            self.orchestrator = CentaurOrchestrator(
                self.settings,
                self.agent_manager,
                self.digital_twin_manager
            )
            await self.orchestrator.initialize()
            
            # Initialize Recursive Improvement Engine
            logger.info("🔄 Initializing Recursive Improvement Engine...")
            self.recursive_engine = RecursiveImprovementEngine(
                self.settings,
                self.orchestrator,
                self.agent_manager
            )
            await self.recursive_engine.initialize()
            
            logger.info("✅ All system components initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize system components: {e}")
            raise
    
    async def start(self):
        """Start the Centaur System"""
        logger.info("🚀 Starting Centaur System...")
        
        try:
            self._running = True
            
            # Start all components
            if self.digital_twin_manager:
                await self.digital_twin_manager.start()
            
            if self.agent_manager:
                await self.agent_manager.start()
            
            if self.orchestrator:
                await self.orchestrator.start()
            
            if self.recursive_engine:
                await self.recursive_engine.start()
            
            logger.info("🎉 Centaur System is now running!")
            logger.info("🧠 Multi-agent coordination active")
            logger.info("🔄 Recursive improvement engine online")
            logger.info("🎯 Digital twin cognitive modeling enabled")
            
            # Start the main application loop
            await self._main_loop()
            
        except Exception as e:
            logger.error(f"❌ Failed to start Centaur System: {e}")
            raise
    
    async def shutdown(self):
        """Gracefully shutdown the Centaur System"""
        logger.info("🛑 Shutting down Centaur System...")
        
        try:
            self._running = False
            
            # Shutdown components in reverse order
            if self.recursive_engine:
                await self.recursive_engine.shutdown()
            
            if self.orchestrator:
                await self.orchestrator.shutdown()
            
            if self.agent_manager:
                await self.agent_manager.shutdown()
            
            if self.digital_twin_manager:
                await self.digital_twin_manager.shutdown()
            
            logger.info("✅ Centaur System shutdown complete")
            
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")
            raise
    
    async def _main_loop(self):
        """Main application event loop"""
        logger.info("🔄 Starting main application loop...")
        
        while self._running:
            try:
                # Perform periodic system maintenance
                await self._periodic_maintenance()
                
                # Wait before next iteration
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}")
                await asyncio.sleep(5)  # Brief pause before retrying
    
    async def _periodic_maintenance(self):
        """Perform periodic system maintenance tasks"""
        # This can include:
        # - Health checks
        # - Performance monitoring
        # - Memory cleanup
        # - Status updates
        pass
    
    @property
    def is_running(self) -> bool:
        """Check if the system is running"""
        return self._running
    
    def get_status(self) -> dict:
        """Get current system status"""
        return {
            "running": self._running,
            "components": {
                "digital_twin_manager": self.digital_twin_manager is not None,
                "agent_manager": self.agent_manager is not None,
                "orchestrator": self.orchestrator is not None,
                "recursive_engine": self.recursive_engine is not None,
            }
        }
