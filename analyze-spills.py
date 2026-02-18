import pandas as pd
from typing import Optional
from config import CONFIG_VAR_1, CONFIG_VAR_2  # Example imports from config.py


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
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: No data found in the file.")
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
    aggregated_data = data.groupby('category').sum().reset_index()  # Example aggregation
    return aggregated_data


def visualize(data: pd.DataFrame) -> None:
    """
    Visualize the aggregated data using matplotlib.

    Parameters:
        data (pd.DataFrame): The aggregated data to visualize.
    """
    import matplotlib.pyplot as plt
    plt.bar(data['category'], data['total'])  # Example plot
    plt.xlabel('Category')
    plt.ylabel('Total')
    plt.title('Aggregated Spills Data')
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
        visualize(aggregated_df)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    FILEPATH = CONFIG_VAR_1  # Example of getting the file path from config
    main(FILEPATH)
