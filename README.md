# Weather Data Pipeline & Exploratory Analysis

A Python data pipeline for collecting, transforming and analysing weather observations from Portuguese cities. Originally developed for a Master's project (2021–2022) and updated in 2026 as a reproducible portfolio project.

**Academic context:** Master's Degree in **Business Intelligence and Analytics**, Instituto Politécnico de Tomar (English description used for this portfolio).

## At a glance

- **11 cities** and **1,243 historical observations** collected between 29 December 2021 and 3 January 2022, included for an offline demonstration.
- **OpenWeather API** ingestion with explicit Portugal (`PT`) validation to reduce ambiguous city-name matches.
- **pandas** transformations, **geopy** geodesic distance calculations and timestamped **JSON/CSV** snapshots.
- A **Jupyter Notebook** for exploratory data analysis, temperature/humidity visualisations and an interactive **Folium** map.
- **4 offline pytest tests** and a GitHub Actions workflow configured to run them on pushes and pull requests.

> This is a portfolio and learning project, not a production service. Live API ingestion requires your own OpenWeather API key and an internet connection.

## Architecture

```text
OpenWeather API (live mode)             Historic sample CSV (offline mode)
            |                                        |
            v                                        |
src/pipeline.py                                     |
  - fetch + validate city (PT)                      |
  - extract structured fields                       |
  - compute distance to reference city              |
  - timestamp each collection                       |
            |                                        |
            v                                        |
 data/runs/*_weather.json + .csv                    |
 data/latest_weather.json + .csv                    |
            |                                        |
            +-------------------+--------------------+
                                |
                                v
                 notebooks/Weather_Analysis_Portfolio.ipynb
                      pandas / Matplotlib / Folium
```

## Repository layout

```text
weather-data-pipeline/
├── .github/workflows/tests.yml        # GitHub Actions: offline tests
├── notebooks/Weather_Analysis_Portfolio.ipynb
├── sample_data/historic_weather_2021_2022.csv
├── scripts/run_pipeline.py            # CLI entry point
├── scripts/run_pipeline.bat           # Windows helper
├── src/pipeline.py                     # Extraction, transformation, persistence
├── tests/test_pipeline.py             # Offline pytest tests
├── legacy/                             # Preserved academic implementation
├── .env.example
├── .gitignore
└── requirements.txt
```

## Quick start (Windows / VS Code)

From the repository root, with Python 3.13 installed:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

In VS Code, open `notebooks/Weather_Analysis_Portfolio.ipynb`, select the Python kernel from `.venv`, then choose **Run All**. The default `DATA_SOURCE = "sample"` uses the included historical CSV and does **not** require an API key. The notebook contains saved outputs so its analyses can also be reviewed on GitHub.

## Run a live collection

1. Copy `.env.example` to a new `.env` file at the repository root.
2. Replace the placeholder with your **own** OpenWeather API key in `.env`. Never commit this file or paste the key into code or screenshots.
3. Run the pipeline from the repository root:

```powershell
.\.venv\Scripts\python.exe -m scripts.run_pipeline --ref-city "Peniche" --cities "Tomar" "Coimbra" "Braga" "Beja" --out-dir data/runs
```

The pipeline writes timestamped `.json` and `.csv` files under `data/runs/` and updates `data/latest_weather.json` and `data/latest_weather.csv`. These generated files are intentionally excluded from Git.

To analyse accumulated live snapshots, change the notebook setting to:

```python
DATA_SOURCE = "runs"
```

Then run all notebook cells again. Multiple collections over time are needed for meaningful time-series comparisons.

## Data analysis

The notebook demonstrates:

- Data loading, type conversion, cleaning and missing-value checks with **pandas**
- Exploratory summaries and temperature/humidity visualisation
- Basic correlation analysis (subject to data coverage)
- An interactive **Folium** map of the selected Portuguese cities

### Historical data-quality issue: Beja

The original 2021–2022 collection contains a ~1,652 km distance for **Beja**, because a weather lookup resolved to Beja, Tunisia. The historical observations and distance are preserved to document this issue. The offline map uses approximate Portuguese city-centre coordinates for illustration. The modern pipeline requests `city,PT` and validates that OpenWeather returns `PT` to mitigate this ambiguity. Map distances are geodesic (straight-line), not road distances.

## Tests and automation

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The 4 offline tests cover normal pipeline output, explicit output paths, empty city lists and rejection of non-Portuguese locations. API responses are mocked; these tests **do not** verify live OpenWeather availability. A workflow in `.github/workflows/tests.yml` runs them on GitHub Actions; check the **Actions** tab for the latest result.

## Limitations and possible extensions

- Live API calls depend on an external service and a valid, active API key.
- The dataset is small and historical; the included sample is suitable for demonstrating the analysis workflow, not for current meteorological conclusions.
- There is no deployed scheduler or database service. Potential future improvements include periodic scheduling, PostgreSQL storage and additional integration tests.
- The `legacy/` folder preserves the original academic code for reference and is not the supported execution path.

## Author

**Soraia Pedro Tarrinha** — Python, SQL and data analysis
