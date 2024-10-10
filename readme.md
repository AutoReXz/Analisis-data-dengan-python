# Bike Rental Analysis Dashboard

## Overview
This project provides a comprehensive analysis of bike rental patterns using Streamlit. The dashboard offers insights into daily patterns, seasonal trends, and weather impacts on bike rentals.

## Features
- Interactive filters for year, season, and time range
- Key performance metrics display
- Multiple analysis tabs:
  - Daily Patterns
  - Seasonal Analysis
  - Weather Impact
- Insights and business recommendations

## Installation
1. Clone this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the dashboard:
   ```
   streamlit run dashboard.py
   ```

## Data
The dashboard uses two datasets:
- day.csv: Daily aggregated rental data
- hour.csv: Hourly rental data

Both datasets should be placed in a 'Dataset' folder in the project directory.

## Structure
- `dashboard.py`: Main application file
- `Dataset/`: Folder containing required datasets
  - `day.csv`
  - `hour.csv`

## Dependencies
See `requirements.txt` for a full list of dependencies.

## Author
Galang
