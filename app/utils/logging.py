import logging
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class CustomFormatter(logging.Formatter):
    """Custom log formatter with color-coding for terminal output"""
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[91m', # Red
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record):
        log_message = super().format(record)
        # Add color if terminal supports it
        if sys.stdout.isatty():
            return f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}{log_message}{self.COLORS['RESET']}"
        return log_message

class JSONLogFormatter(logging.Formatter):
    """Formatter for structured JSON logs"""
    def format(self, record):
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
            'path': record.pathname,
            'line': record.lineno
        }
        
        # Add exception info if exists
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
            
        # Add extra attributes from record
        for key, value in record.__dict__.items():
            if key not in ('args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
                          'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module',
                          'msecs', 'message', 'msg', 'name', 'pathname', 'process',
                          'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName'):
                log_data[key] = value
                
        return json.dumps(log_data)

def setup_logging(log_level="INFO", log_format="standard", log_file=None):
    """Set up logging configuration
    
    Args:
        log_level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format (str): Format type ("standard", "color", "json")
        log_file (str, optional): Path to log file
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if log_format == "color":
        formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    elif log_format == "json":
        formatter = JSONLogFormatter()
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        handlers.append(file_handler)
    
    # Add handlers to logger
    for handler in handlers:
        logger.addHandler(handler)
    
    return logger

class PerformanceTimer:
    """Utility for timing operations"""
    def __init__(self, name=None):
        self.name = name or "Operation"
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        
    @property
    def elapsed(self):
        """Get elapsed time in seconds"""
        if self.start_time is None:
            return 0
        end = self.end_time or time.time()
        return end - self.start_time
        
    def log(self, logger=None, level="INFO"):
        """Log the timing information"""
        if logger is None:
            logger = logging.getLogger()
        
        log_method = getattr(logger, level.lower())
        log_method(f"{self.name} completed in {self.elapsed:.4f} seconds")
        
    def as_dict(self):
        """Return timing information as a dictionary"""
        return {
            'operation': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'elapsed_seconds': self.elapsed
        }