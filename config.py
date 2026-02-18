"""
Configuration settings for data analysis scripts.

This module centralizes all configuration values including file paths,
thresholds, and output settings.
"""

from typing import Dict
from datetime import datetime

# ============================================================================
# OZONE ANALYSIS CONFIGURATION
# ============================================================================

OZONE_FILES: Dict[str, str] = {
    '2022': 'daily_44201_2022.csv',
    '2023': 'daily_44201_2023.csv',
    '2024': 'daily_44201_2024.csv',
    '2025': 'daily_44201_2025.csv'
}

# Denver County identifiers
DENVER_STATE_CODE = 8
DENVER_COUNTY_CODE = 31

# Federal Ozone Standard (ppm)
FEDERAL_OZONE_LIMIT = 0.070

# Ozone analysis output
OZONE_OUTPUT_FILE = 'ozone_comparison_multiyear.png'
OZONE_TITLE = 'Denver Ozone Trends: 2022 - 2025'

# ============================================================================
# SPILLS ANALYSIS CONFIGURATION
# ============================================================================

SPILLS_INPUT_FILE = 'Spills.xlsx - Spills.csv'
SPILLS_OUTPUT_FILE = 'spill_analysis_final.png'
SPILLS_TITLE = 'Colorado Oil & Gas Spills: 2018 - 2025\nDid the "Mission Change" reduce accidents?'

# Date when SB-19-181 was signed
SB181_INTERVENTION_DATE = datetime(2019, 4, 16)

# Date range for filtering spill data
SPILLS_START_DATE = '2018-01-01'
SPILLS_END_DATE = '2025-12-31'

# Spills rolling average window (months)
SPILLS_ROLLING_AVERAGE_WINDOW = 6

# ============================================================================
# OZONE VISUALIZATION SETTINGS
# ============================================================================

OZONE_SUMMER_MONTHS = (5, 9)  # May through September

OZONE_STYLE_CONFIG = {
    '2022': {'color': '#bdc3c7', 'width': 1.5, 'style': '--', 'label': '2022'},
    '2023': {'color': '#7f8c8d', 'width': 1.5, 'style': '--', 'label': '2023'},
    '2024': {'color': '#2980b9', 'width': 2.0, 'style': '-', 'label': '2024'},
    '2025': {'color': '#c0392b', 'width': 3.0, 'style': '-', 'label': '2025'}
}

# ============================================================================
# GENERAL VISUALIZATION SETTINGS
# ============================================================================

FIGURE_WIDTH = 12
FIGURE_HEIGHT = 7
OUTPUT_DPI = 300
FONT_SIZE_TITLE = 16
FONT_SIZE_LABEL = 12
FONT_SIZE_TICK = 10

# CSV encoding (common for government data files)
CSV_ENCODING = 'ISO-8859-1'

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'