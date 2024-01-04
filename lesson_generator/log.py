import logging
import os

# Ensures the logs directory exists
if not os.path.exists('logs'):
    os.mkdir('logs')

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

# Get a logger instance for the app
logger = logging.getLogger('lesson_generator')
