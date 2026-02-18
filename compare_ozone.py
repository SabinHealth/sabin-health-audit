import logging
from config import SOME_CONFIG_CONSTANT

logger = logging.getLogger(__name__)


def compare_ozone(data: list) -> dict:
    """
    Compares ozone levels from the provided data list and returns 
    a summary of the comparison results.

    Parameters:
    - data (list): A list of dictionaries containing ozone data

    Returns:
    - dict: A dictionary summarizing the comparison results
    """
    if not isinstance(data, list):
        logger.error('Expected a list, got %s', type(data).__name__)
        raise ValueError('The input data must be a list.') 

    result = {}
    try:
        for entry in data:
            if 'ozone_level' not in entry:
                logger.warning('Entry missing ozone level: %s', entry)
                continue
            ozone_level = entry['ozone_level']
            # Assuming the constant is used for comparison
            if ozone_level > SOME_CONFIG_CONSTANT:
                result[entry['id']] = 'Exceeds allowable level'
            else:
                result[entry['id']] = 'Within safe levels'

    except Exception as e:
        logger.exception('An error occurred during comparison: %s', str(e))
        raise

    return result
