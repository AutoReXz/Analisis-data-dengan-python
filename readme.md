# Bike Rental Analysis Dashboard

This coursework project uses Python to explore how bike rentals vary by hour, season, and weather. It includes an exploratory notebook and a Streamlit dashboard built from historical Capital Bikeshare data.

## What to Explore

- Compare average hourly rentals on working and non-working days.
- Inspect seasonal and monthly patterns and compare rental counts across weather categories.
- Use the year filter across the dashboard, the hour range for hourly patterns, and the season selection for daily summaries. Keep at least one season selected.

## Run Locally

From the repository root, using Python 3.12:

```bash
python -m venv .venv
```

Activate the environment with `source .venv/bin/activate` on macOS or Linux, or `\.venv\Scripts\Activate.ps1` in Windows PowerShell. Then run:

```bash
python -m pip install -r requirements.txt "scipy<1.16"
python -m streamlit run dashboard.py
```

The SciPy constraint keeps the pinned statsmodels release compatible with the Plotly trendline. Open the local URL shown by Streamlit. The CSVs are included in `Dataset/` and the dashboard reads them from that path.

## Repository Contents

- [Proyek_Analisis_Data.ipynb](Proyek_Analisis_Data.ipynb) — Data inspection, exploratory analysis, visualizations, and interpretation.
- [dashboard.py](dashboard.py) — Streamlit dashboard with pandas and Plotly.
- [Dataset/](Dataset/) — Daily and hourly rental counts and accompanying weather records.
- [requirements.txt](requirements.txt) — Pinned Python dependencies for the dashboard.

## Data Attribution

The Bike Sharing Dataset was prepared by Hadi Fanaee-T using Capital Bikeshare records from 2011 and 2012. The repository includes the original data notes and citation. The dashboard describes patterns in that observation period.

[UCI Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) · [Original data notes](Dataset/Readme.txt)
