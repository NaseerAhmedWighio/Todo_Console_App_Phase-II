"""Logging configuration for Todo App backend."""
import logging
from datetime import datetime
import sys
from typing import Optional

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log"),
    ],
)

logger = logging.getLogger(__name__)


def log_user_action(user_id: str, action: str, details: Optional[dict] = None):
    """Log user actions for audit trail."""
    logger.info(f"User {user_id} performed {action}", extra={"details": details})


def log_api_request(endpoint: str, method: str, user_id: Optional[str] = None, duration_ms: Optional[float] = None):
    """Log API requests for monitoring."""
    log_msg = f"API request: {method} {endpoint}"
    if user_id:
        log_msg += f" by user {user_id}"
    if duration_ms:
        log_msg += f" took {duration_ms:.2f}ms"

    logger.info(log_msg)


def log_error(error: Exception, context: Optional[str] = None):
    """Log errors with context."""
    logger.error(f"Error occurred{' in ' + context if context else ''}: {str(error)}", exc_info=True)