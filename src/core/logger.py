"""
Logging configuration for the Centaur System
"""

import logging
import logging.config
import sys
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_format: str = "detailed"):
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Define log formats
    formats = {
        "simple": "%(levelname)s - %(message)s",
        "detailed": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "json": '{"timestamp": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
    }
    
    # Logging configuration
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": formats.get(log_format, formats["detailed"])
            },
            "colored": {
                "()": ColoredFormatter,
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "colored",
                "stream": sys.stdout
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "standard",
                "filename": str(log_dir / "centaur.log"),
                "maxBytes": 100 * 1024 * 1024,  # 100MB
                "backupCount": 10
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "standard",
                "filename": str(log_dir / "centaur_errors.log"),
                "maxBytes": 50 * 1024 * 1024,  # 50MB
                "backupCount": 5
            }
        },
        "loggers": {
            "centaur": {
                "level": log_level,
                "handlers": ["console", "file", "error_file"],
                "propagate": False
            },
            "agents": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            },
            "coordination": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            },
            "recursive": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            }
        },
        "root": {
            "level": log_level,
            "handlers": ["console", "file", "error_file"]
        }
    }
    
    logging.config.dictConfig(config)
    
    # Log startup message
    logger = logging.getLogger("centaur.setup")
    logger.info("🔧 Logging system initialized")
    logger.info(f"📊 Log level: {log_level}")
    logger.info(f"📁 Log directory: {log_dir.absolute()}")


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        # Add color to the log level
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        
        # Add emoji based on log level
        emojis = {
            'DEBUG': '🔍',
            'INFO': '📋',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'CRITICAL': '🚨'
        }
        
        original_levelname = record.levelname.replace(
            self.COLORS.get(record.levelname.split('\033')[1].split('m')[1] if '\033' in record.levelname else record.levelname, ''),
            ''
        ).replace(self.COLORS['RESET'], '')
        
        if original_levelname in emojis:
            record.msg = f"{emojis[original_levelname]} {record.msg}"
        
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(f"centaur.{name}")


# Create common loggers
main_logger = get_logger("main")
agent_logger = get_logger("agents")
coordination_logger = get_logger("coordination")
recursive_logger = get_logger("recursive")
health_logger = get_logger("health")
