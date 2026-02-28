import pandas as pd
import matplotlib.pyplot as plt
import logging
from config import (
    ENCAMPMENTS_INPUT_FILE,
    ENCAMPMENTS_TARGET_SUMMARIES,
    ENCAMPMENTS_OUTPUT_CSV,
    ENCAMPMENTS_OUTPUT_PNG,
    ENCAMPMENTS_TITLE,
    LOG_FORMAT,
    LOG_LEVEL
)

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def load_data(filepath: str) -> pd.DataFrame:
    """Load the 311 Dataset."""
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        logger.error(f"Failed to load data from {filepath}: {e}")
        raise


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for Encampment & Sweep specific case types and clean dates."""
    df_filtered = df[df['Case Summary'].isin(ENCAMPMENTS_TARGET_SUMMARIES)].copy()
    df_filtered['Date'] = pd.to_datetime(df_filtered['Case Created Date'])
    df_filtered = df_filtered.dropna(subset=['Date'])
    df_filtered['YearMonth'] = df_filtered['Date'].dt.to_period('M')
    return df_filtered


def aggregate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate by month and save to CSV."""
    monthly_counts = df.groupby('YearMonth').size().reset_index(name='Encampment_Reports')
    monthly_counts.to_csv(ENCAMPMENTS_OUTPUT_CSV, index=False)
    return monthly_counts


def visualize(monthly_counts: pd.DataFrame) -> None:
    """Build the Sabin Health Chart."""
    plt.figure(figsize=(10, 6))

    # Remove the incomplete Feb 2026 data point for clean charting
    plot_data = monthly_counts[monthly_counts['YearMonth'] < '2026-02'].copy()
    plot_data['DateObj'] = plot_data['YearMonth'].dt.to_timestamp()

    # Dual overlay: Bar chart for volume + Line chart for trend (Sabin Colors)
    plt.bar(plot_data['DateObj'], plot_data['Encampment_Reports'], color='#bdc3c7', alpha=0.4, width=20)
    plt.plot(plot_data['DateObj'], plot_data['Encampment_Reports'], marker='o', color='#c0392b', linewidth=3, label='311 Encampment Reports')

    plt.title(ENCAMPMENTS_TITLE, fontsize=14, color='#2c3e50', pad=15)
    plt.ylabel('Number of Citizen Reports', fontweight='bold', color='#2c3e50')
    plt.xlabel('Month', fontweight='bold', color='#2c3e50')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(ENCAMPMENTS_OUTPUT_PNG)
    logger.info(f"Chart saved to {ENCAMPMENTS_OUTPUT_PNG}")


def main():
    try:
        df = load_data(ENCAMPMENTS_INPUT_FILE)
        df_cleaned = clean_data(df)
        monthly_counts = aggregate_data(df_cleaned)
        visualize(monthly_counts)
    except Exception as e:
        logger.error(f"An error occurred during encampment analysis: {e}")


if __name__ == '__main__':
    main()
