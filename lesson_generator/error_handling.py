from lesson_generator.log import logger
import sys

class LessonGenerationError(Exception):
    """Custom exception class for Lesson generation-related errors."""

def handle_exception(exc_type, exc_value, exc_traceback):
    """Global function to handle uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Replace the default exception handler with our custom one
sys.excepthook = handle_exception
