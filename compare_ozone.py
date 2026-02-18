import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os

# --- CONFIGURATION ---
# Ensure these filenames match exactly what is in your folder
FILES = {
    '2022': 'daily_44201_2022.csv',
    '2023': 'daily_44201_2023.csv',
    '2024': 'daily_44201_2024.csv',
    '2025': 'daily_44201_2025.csv'
}

# Denver County (031)
STATE_CODE = 8
COUNTY_CODE = 31

# Federal Ozone Standard (0.070 ppm)
LIMIT = 0.070

def load_and_prep(filename, year_label):
    # Check if file exists before trying to load
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found. Skipping {year_label}.")
        return None

    print(f"Loading {year_label} data...")
    df = pd.read_csv(filename, usecols=['State Code', 'County Code', 'Date Local', 'Arithmetic Mean'])
    
    # Filter for Denver
    denver = df[(df['State Code'] == STATE_CODE) & (df['County Code'] == COUNTY_CODE)].copy()
    
    # Convert dates
    denver['Date Local'] = pd.to_datetime(denver['Date Local'])
    
    # Get daily max (worst reading of the day across all monitors)
    daily = denver.groupby('Date Local')['Arithmetic Mean'].max().reset_index()
    
    # CRITICAL TRICK: "Normalize" the year to 2000 so we can overlay them
    daily['PlotDate'] = daily['Date Local'].apply(lambda x: x.replace(year=2000))
    
    daily['Year'] = year_label
    return daily

def run_comparison():
    # 1. Load Data for all years
    data_frames = []
    for year, filename in FILES.items():
        df = load_and_prep(filename, year)
        if df is not None:
            data_frames.append(df)
    
    if not data_frames:
        print("No data files found! Check your folder.")
        return

    # 2. Combine into one dataset
    combined = pd.concat(data_frames)
    
    # 3. Filter to Summer Months (May - Sept)
    # Note: 2025 might only have May/June data, which is fine.
    combined = combined[combined['PlotDate'].dt.month.between(5, 9)]

    # --- VISUALIZATION ---
    print("Generating Comparison Chart...")
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 7))

    # Define Custom Styles for each year
    # Older years = Thinner, Grey/Blue
    # Newest year (2025) = Thick, Bold Red (to see current status)
    styles = {
        '2022': {'color': '#bdc3c7', 'width': 1.5, 'style': '--'}, # Grey dashed
        '2023': {'color': '#7f8c8d', 'width': 1.5, 'style': '--'}, # Darker Grey dashed
        '2024': {'color': '#2980b9', 'width': 2.0, 'style': '-'},  # Blue solid
        '2025': {'color': '#c0392b', 'width': 3.0, 'style': '-'}   # Bold Red solid
    }

    # Plot each year manually to control style perfectly
    for year in FILES.keys():
        # Only plot if we actually loaded data for this year
        year_data = combined[combined['Year'] == year]
        if not year_data.empty:
            s = styles.get(year, {'color': 'black', 'width': 1}) # Fallback style
            sns.lineplot(
                data=year_data, 
                x='PlotDate', 
                y='Arithmetic Mean', 
                color=s['color'], 
                linewidth=s['width'], 
                linestyle=s['style'],
                label=year, # Just "2024", no extra text
                errorbar=None # Removes confidence ribbons for cleaner look
            )

    # Add The Danger Line (Black)
    plt.axhline(y=LIMIT, color='black', linewidth=1.5, linestyle='-', label='Federal Limit')

    # Formatting
    plt.title('Denver Ozone Trends: 2022 - 2025', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Ozone Concentration (ppm)', fontsize=12)
    plt.xlabel('Summer Season', fontsize=12)
    
    # Fix X-Axis to show Month Names
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    plt.legend(loc='upper right')
    plt.tight_layout()
    
    plt.savefig('ozone_comparison_multiyear.png', dpi=300)
    print("Success! Chart saved as 'ozone_comparison_multiyear.png'")
    # plt.show() # Uncomment if you want to see it pop up

if __name__ == "__main__":
    run_comparison()