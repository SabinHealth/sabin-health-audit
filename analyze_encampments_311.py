import logging

import matplotlib.pyplot as plt
import pandas as pd

from config import (
    ENCAMPMENTS_CUTOFF_DATE,
    ENCAMPMENTS_INPUT_FILE,
    ENCAMPMENTS_OUTPUT_CSV,
    ENCAMPMENTS_OUTPUT_PNG,
    ENCAMPMENTS_TARGET_SUMMARIES,
    ENCAMPMENTS_TITLE,
    FIGURE_HEIGHT,
    FIGURE_WIDTH,
    OUTPUT_DPI,
)

logger = logging.getLogger(__name__)


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the 311 dataset from a CSV file.

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError as e:
        logger.error('File not found: %s', e)
        raise
    except pd.errors.EmptyDataError:
        logger.error('No data found in the file.')
        raise


def filter_encampments(data: pd.DataFrame, target_summaries: list) -> pd.DataFrame:
    """
    Filter rows matching encampment and sweep-related case types.

    Parameters:
        data (pd.DataFrame): Raw 311 data.
        target_summaries (list): List of case summary strings to include.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    return data[data['Case Summary'].isin(target_summaries)].copy()


def aggregate_monthly(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dates and aggregate reports by month.

    Parameters:
        data (pd.DataFrame): Filtered encampment data.

    Returns:
        pd.DataFrame: Monthly report counts.
    """
    data = data.copy()
    data['Date'] = pd.to_datetime(data['Case Created Date'])
    data = data.dropna(subset=['Date'])
    data['YearMonth'] = data['Date'].dt.to_period('M')
    monthly_counts = data.groupby('YearMonth').size().reset_index(name='Encampment_Reports')
    return monthly_counts


def save_csv(data: pd.DataFrame, output_path: str) -> None:
    """
    Save aggregated data to a CSV file.

    Parameters:
        data (pd.DataFrame): Data to save.
        output_path (str): Path to the output CSV file.
    """
    data.to_csv(output_path, index=False)
    logger.info('Saved CSV to %s', output_path)


def build_chart(monthly_counts: pd.DataFrame, cutoff_date: str, output_path: str, title: str) -> None:
    """
    Build and save the encampment trend chart.

    Parameters:
        monthly_counts (pd.DataFrame): Monthly aggregated data.
        cutoff_date (str): Exclude months at or after this date (e.g. '2026-02').
        output_path (str): Path to save the chart image.
        title (str): Chart title.
    """
    plot_data = monthly_counts[monthly_counts['YearMonth'] < cutoff_date].copy()
    plot_data['DateObj'] = plot_data['YearMonth'].dt.to_timestamp()

    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    plt.bar(plot_data['DateObj'], plot_data['Encampment_Reports'], color='#bdc3c7', alpha=0.4, width=20)
    plt.plot(plot_data['DateObj'], plot_data['Encampment_Reports'], marker='o', color='#c0392b', linewidth=3, label='311 Encampment Reports')

    plt.title(title, fontsize=14, color='#2c3e50', pad=15)
    plt.ylabel('Number of Citizen Reports', fontweight='bold', color='#2c3e50')
    plt.xlabel('Month', fontweight='bold', color='#2c3e50')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_path, dpi=OUTPUT_DPI)
    logger.info('Saved chart to %s', output_path)


def main() -> None:
    """
    Main function to run the encampments 311 analysis.
    """
    try:
        data = load_data(ENCAMPMENTS_INPUT_FILE)
        filtered = filter_encampments(data, ENCAMPMENTS_TARGET_SUMMARIES)
        monthly_counts = aggregate_monthly(filtered)
        save_csv(monthly_counts, ENCAMPMENTS_OUTPUT_CSV)
        build_chart(monthly_counts, ENCAMPMENTS_CUTOFF_DATE, ENCAMPMENTS_OUTPUT_PNG, ENCAMPMENTS_TITLE)
    except Exception as e:
        logger.exception('An error occurred: %s', e)
        raise


if __name__ == '__main__':
    main()
