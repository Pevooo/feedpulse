import logging
import os
import warnings
import functools


def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is deprecated and may be removed in future versions.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)

    return wrapper


def log(message: str, level: str = "info"):
    log_path = "log.log"
    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("feedpulse")
    logger.setLevel(logging.INFO)

    # Prevent adding duplicate handlers
    if not logger.hasHandlers():
        # File handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)

        # Console handler (for systemd journal)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(console_handler)

    # Log the message
    level = level.lower()
    if level == "debug":
        logger.debug(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)
    else:
        logger.info(message)
