import logging
import os
from datetime import datetime

def setup_logger(name: str = "Saksham", log_file: str = "system_logs.log") -> logging.Logger:
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(levelname)-8s | %(message)s'
    )
    
    # File handler (detailed logs)
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler (less verbose)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_agent_action(logger: logging.Logger, agent_name: str, action: str, details: str = ""):
    message = f"[{agent_name}] {action}"
    if details:
        message += f" | {details}"
    logger.info(message)


def log_error_with_context(logger: logging.Logger, error: Exception, context: str = ""):
    import traceback
    
    error_msg = f"ERROR: {str(error)}"
    if context:
        error_msg = f"{context} - {error_msg}"
    
    logger.error(error_msg)
    logger.debug(f"Traceback:\n{traceback.format_exc()}")