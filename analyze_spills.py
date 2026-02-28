import pandas as pd
import logging
from config import SPILLS_INPUT_FILE, SPILLS_TITLE, LOG_FORMAT, LOG_LEVEL

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load data from the specified CSV file.

    Parameters:
        filepath (str): The path to the data file.

    Returns:
        pd.DataFrame: Data loaded into a pandas DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        logger.error("Error: No data found in the file.")
        raise


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the provided DataFrame by removing null values and duplicates.

    Parameters:
        data (pd.DataFrame): The input DataFrame with spills data.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    data_cleaned = data.dropna()  # Remove rows with null values
    data_cleaned = data_cleaned.drop_duplicates()  # Remove duplicate rows
    return data_cleaned


def aggregate_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate the cleaned data by specific metrics.

    Parameters:
        data (pd.DataFrame): The cleaned DataFrame.

    Returns:
        pd.DataFrame: Aggregated results.
    """
    # Assuming the data has 'category' and 'total' columns based on original visualize function
    aggregated_data = data.groupby('category').sum().reset_index()
    return aggregated_data


def visualize(data: pd.DataFrame) -> None:
    """
    Visualize the aggregated data using matplotlib.

    Parameters:
        data (pd.DataFrame): The aggregated data to visualize.
    """
    import matplotlib.pyplot as plt
    plt.bar(data['category'], data['total'])
    plt.xlabel('Category')
    plt.ylabel('Total')
    plt.title(SPILLS_TITLE)
    plt.show()


def main(filepath: str) -> None:
    """
    Main function to execute the data analysis.

    Parameters:
        filepath (str): The path to the input data file.
    """
    try:
        data = load_data(filepath)
        clean_data_df = clean_data(data)
        aggregated_df = aggregate_data(clean_data_df)
        logger.info("Aggregated Data summary:")
        logger.info(aggregated_df.head())
        # visualize(aggregated_df) # Commented out for automated environments
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == '__main__':
    main(SPILLS_INPUT_FILE)
