import logging

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Utility Functions for Logging

def log_info(message):
    logging.info(message)


def log_error(message):
    logging.error(message)


# Error Handling Utility

def handle_error(error):
    log_error(f'Error occurred: {error}')
    raise Exception(error)


# Data Validation Helpers

def validate_input(data, data_type):
    if not isinstance(data, data_type):
        handle_error(f'Invalid input: Expected {data_type.__name__}, got {type(data).__name__}')
    log_info('Input validation successful')


# Visualization Helpers

def visualize_data(data):
    # Placeholder for visualization logic (e.g., plotting data)
    log_info('Visualizing data...')
