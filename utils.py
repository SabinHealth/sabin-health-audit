import logging
from config import LOG_FORMAT, LOG_LEVEL

# Logging Configuration
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


# Error Handling Utility

def handle_error(error):
    logger.error(f'Error occurred: {error}')
    raise Exception(error)


# Data Validation Helpers

def validate_input(data, data_type):
    if not isinstance(data, data_type):
        handle_error(f'Invalid input: Expected {data_type.__name__}, got {type(data).__name__}')
    logger.info('Input validation successful')


# Visualization Helpers

def visualize_data(data):
    # Placeholder for visualization logic (e.g., plotting data)
    logger.info('Visualizing data...')
