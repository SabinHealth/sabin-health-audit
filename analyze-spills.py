import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# --- CONFIGURATION ---
FILE_NAME = 'Spills.xlsx - Spills.csv'
SB181_DATE = pd.Timestamp('2019-04-16') # Date SB-19-181 was signed

def analyze_spills():
    print("Loading Spill Data...")
    
    # Load data (using ISO-8859-1 encoding which is common for government CSVs)
    try:
        df = pd.read_csv(FILE_NAME, encoding='ISO-8859-1', low_memory=False)
    except FileNotFoundError:
        print(f"Error: Could not find {FILE_NAME}. Please check the filename.")
        return

    # 1. Clean Dates
    # The relevant column in your file is 'Date of Discovery'
    df['Date of Discovery'] = pd.to_datetime(df['Date of Discovery'], errors='coerce')
    
    # Filter to relevant years (2018 - Present)
    # We remove rows with no date and filter for the modern era
    df = df[(df['Date of Discovery'] >= '2018-01-01') & (df['Date of Discovery'] <= '2025-12-31')].copy()
    
    # 2. Aggregation: Unique Spills per Month
    # We group by 'Tracking #' to count unique spill events, avoiding duplicate 'Supplemental' reports
    unique_spills = df.groupby('Tracking #')['Date of Discovery'].min().reset_index()
    monthly_spills = unique_spills.groupby(pd.Grouper(key='Date of Discovery', freq='M')).size().reset_index(name='Spill_Count')
    
    # 3. Visualization
    print("Generating Chart...")
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 7))
    
    # Plot the raw monthly count (Grey line)
    plt.plot(monthly_spills['Date of Discovery'], monthly_spills['Spill_Count'], 
             color='#bdc3c7', linewidth=1.5, label='Monthly Reports (Raw)', alpha=0.6)
    
    # Add Trend Line (6-Month Rolling Average) - Bold Orange
    monthly_spills['MA_6'] = monthly_spills['Spill_Count'].rolling(window=6).mean()
    plt.plot(monthly_spills['Date of Discovery'], monthly_spills['MA_6'], 
             color='#e67e22', linewidth=3, label='6-Month Trend')

    # Add the "Intervention Line" (SB-181)
    plt.axvline(x=SB181_DATE, color='#c0392b', linestyle='--', linewidth=2)
    plt.text(x=SB181_DATE, y=monthly_spills['Spill_Count'].max() * 0.95, s=" SB-19-181 Signed", 
             color='#c0392b', fontweight='bold', verticalalignment='top', rotation=90)

    # Formatting
    plt.title('Colorado Oil & Gas Spills: 2018 - 2025\nDid the "Mission Change" reduce accidents?', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Unique Spill Reports per Month', fontsize=12)
    plt.xlabel('Year', fontsize=12)
    
    # Fix X-axis to show years clearly
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    
    plt.legend(loc='upper left')
    plt.tight_layout()
    
    output_file = 'spill_analysis_final.png'
    plt.savefig(output_file, dpi=300)
    print(f"Success! Chart saved as '{output_file}'")

if __name__ == "__main__":
    analyze_spills()