import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def get_logger(name="ValueLens"):
    """
    Creates and configures a centralized logger for the pipeline.
    Writes timestamped logs to logs/valuelens_{date}.log and streams to console.
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if logger is already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Formatter
        # e.g., 2026-08-30 01:09:00 - ValueLens - INFO - Row count: 500000
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File Handler (Rotating)
        date_str = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_dir, f"valuelens_{date_str}.log")
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
