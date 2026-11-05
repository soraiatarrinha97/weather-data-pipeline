# Weather Data Pipeline & Exploratory Analysis

A Python portfolio project for collecting, transforming, storing, and analysing weather observations from Portuguese cities. Originally developed as academic work in 2021–2022, it has since been reorganised into a modular pipeline with an offline analysis notebook and automated tests.

**Stack:** Python · pandas · OpenWeather API · Requests · geopy · Matplotlib · Folium · Jupyter · pytest

## What the project does

1. **Extract:** request current weather observations from OpenWeather for selected cities, explicitly restricting the search to Portugal.
2. **Transform:** extract temperature, humidity, pressure, wind and geographic coordinates; calculate geodesic distance to a reference city; attach a collection timestamp.
3. **Load:** save each run as JSON and CSV, and update `data/latest_weather.json` and `data/latest_weather.csv`.
4. **Analyse:** use pandas and Jupyter to explore the data, plot trends and correlations, and display city markers on an interactive Folium map.

```text
OpenWeather API ──> Python extraction/transformation ──> JSON & CSV snapshots
                                                           │
Historical academic CSV ────────────────────────────────────┤
                                                           ▼
                                                Jupyter / pandas EDA
                                                           │
                                               Matplotlib + Folium
```

## Demonstration dataset

The repository includes `sample_data/historic_weather_2021_2022.csv`: **1,243 observations from 11 cities**, collected between **29 December 2021 and 3 January 2022** as part of the original academic project. The notebook can analyse this dataset **without an API key**.

**Known historical limitation:** the original data includes an incorrect distance for Beja due to ambiguous geocoding (Beja, Tunisia instead of Beja, Portugal). This value is intentionally identified as a historical data-quality issue. The refactored API pipeline adds `,PT` to city queries and verifies the returned country, rather than claiming that the original data was error-free. Coordinates used for the sample map are approximate presentation coordinates.

## Project structure

```text
weather-data-pipeline/
├── src/pipeline.py                    # Extraction, transformation, persistence
├── scripts/run_pipeline.py            # Command-line interface
├── scripts/run_pipeline.bat           # Optional Conda-based Windows helper
├── notebooks/Weather_Analysis_Portfolio.ipynb
├── sample_data/historic_weather_2021_2022.csv
├── tests/test_pipeline.py             # Offline pytest tests
├── legacy/                            # Original academic implementation
├── .env.example                       # API key placeholder (safe to share)
├── requirements.txt
└── README.md
```

## Quick start — Windows / VS Code

From the repository root, create a virtual environment and install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Open `notebooks/Weather_Analysis_Portfolio.ipynb` in VS Code, select the interpreter from `.venv` as the Jupyter kernel, keep `DATA_SOURCE = "sample"`, and choose **Run All**. This is the easiest way to explore the project; **no key or internet connection to the weather API is needed**.

## Collect new weather observations

1. Create a `.env` file in the repository root by copying `.env.example`.
2. Replace the placeholder in the **local** `.env` with an active OpenWeather API key. Never commit this file.
3. Execute:

```powershell
.\.venv\Scripts\python.exe -m scripts.run_pipeline --ref-city "Peniche" --cities "Tomar" "Coimbra" "Braga" --out-dir data/runs
```

This writes timestamped weather snapshots under `data/runs/` and updates the latest JSON/CSV files under `data/`.

To analyse the new snapshots instead of the academic dataset, set `DATA_SOURCE = "runs"` in the notebook and select **Run All**. Multiple collections over time are needed for meaningful time-series comparisons. The current command performs one collection per invocation; automatic recurring scheduling is **not** part of the Python CLI itself.

## Tests

Four tests run offline with mocked API responses; no OpenWeather key is needed:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

They cover snapshot persistence, explicit output paths, validation of an empty city list and rejection of non-Portuguese locations. GitHub Actions also runs these tests on pushes and pull requests.

## Scope and limitations

- A reproducible **portfolio / academic-to-practical** pipeline, not a production-hosted service.
- API ingestion and snapshot persistence work locally when valid credentials and network access are available; live API integration is not part of the offline test suite.
- No database, Docker deployment, monitoring or automatic scheduling is implemented in the current version.
- The historical Beja geocoding anomaly is documented rather than silently corrected.

## Academic context

Originally developed for the **Mestrado em Analítica e Inteligência Organizacional** (* Analytics and Business Intelligence*), Instituto Politécnico de Tomar, 2021–2022. Subsequently adapted into this portfolio version.

**Author:** Soraia Pedro Tarrinha
