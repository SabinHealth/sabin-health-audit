# Sabin Health Data Audit

This repository contains the Python code used to analyze public health outcomes in Colorado. The findings are published at [SabinHealth.com](https://sabinhealth.com).

## Projects

### 1. Denver Ozone Analysis (`compare_ozone.py`)
Analyzes the effectiveness of the 2024 Reformulated Gasoline (RFG) mandate.
* **Data Source:** EPA Air Quality System (AQS) - Daily Summary Data.
* **Key Findings:** 2024 ozone peaks exceeded the 2022 baseline despite new regulations.

### 2. Oil & Gas Safety Audit (`analyze_spills.py`)
Evaluates the impact of Senate Bill 19-181 on reported spill frequency.
* **Data Source:** ECMC (formerly COGCC) Daily Spill/Release Data.
* **Key Findings:** Reported spills increased by 270% following the implementation of stricter reporting standards.

## How to Run This Code

1. **Install Dependencies:**
   ```bash
   pip install pandas matplotlib seaborn

2. **Download Data:**
Ozone Data:
Go to EPA Outdoor Air Quality Data.

Select "Ozone" -> "2024" -> "Colorado" -> "Denver".

Rename the file to daily_44201_2024.csv.

Oil & Gas Data:

Go to the ECMC Data Dashboard.

Download the "Spills and Releases" dataset.

Rename the file to spills.csv.

3. **Run Scripts**
Navigate to the folder in your terminal and run:

Bash
python3 compare_ozone.py
python3 analyze_spills.py
