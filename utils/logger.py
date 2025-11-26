import logging
import sys
from logging.handlers import RotatingFileHandler

# Create logger
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.DEBUG)

# Create formatters
detailed_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console handler (INFO level)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(detailed_formatter)

# File handler (DEBUG level, rotates at 5MB)
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=5  # Keep 5 backup files
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(detailed_formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Prevent propagation to root logger
logger.propagate = False


def get_logger(name: str):
    """Get a logger instance for a module"""
    return logging.getLogger(name)
