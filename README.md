# Weather Data Pipeline & Exploratory Analysis

## Overview

This project was originally developed as part of a Master's degree in
Business Intelligence and Analytics and later refactored into a
structured and reproducible data pipeline.

The objective of this project is to:

-   Retrieve real-time meteorological data from multiple Portuguese
    cities using the OpenWeather API
-   Compute geographical distances between cities
-   Store structured datasets in JSON and CSV format
-   Maintain historical snapshots of collected data
-   Perform exploratory data analysis and visualization in Jupyter
    Notebook

This repository reflects an evolution from an academic implementation
into a more modular and production-ready structure.

------------------------------------------------------------------------

## What This Project Demonstrates

This project showcases:

-   API integration (OpenWeather API)
-   Data extraction and transformation
-   Geospatial distance computation (geopy)
-   Data persistence (JSON & CSV)
-   Timestamp-based historical tracking
-   Secure environment variable handling (.env)
-   Modular project architecture
-   Exploratory Data Analysis (EDA)
-   Clean dependency management

------------------------------------------------------------------------

## Project Structure

    weather-data-pipeline/
    │
    ├── src/
    │   └── pipeline.py
    │       Core extraction and transformation logic
    │
    ├── scripts/
    │   ├── run_pipeline.py
    │   │   Command-line execution script
    │   └── run_pipeline.bat
    │       Windows helper script
    │
    ├── notebooks/
    │   └── Weather_Analysis_Portfolio.ipynb
    │       Data analysis and visualizations
    │
    ├── data/
    │   └── runs/
    │       Generated historical snapshots (created after execution)
    │
    ├── legacy/
    │       Original academic implementation (kept for reference)
    │
    ├── requirements.txt
    ├── .gitignore
    └── README.md

------------------------------------------------------------------------

## Setup Instructions

### 1. Create a Python Environment

Using Conda:

    conda create -n weather python=3.10 -y
    conda activate weather

Or using venv:

    python -m venv venv
    venv\Scripts\activate

------------------------------------------------------------------------

### 2. Install Dependencies

    pip install -r requirements.txt

------------------------------------------------------------------------

### 3. Configure API Key

Create a `.env` file in the root directory:

    OPENWEATHER_API_KEY=YOUR_API_KEY_HERE

------------------------------------------------------------------------

## Running the Pipeline

From the root directory:

    python -m scripts.run_pipeline --ref-city "Peniche" --cities "Tomar" "Coimbra" "Braga" --out-dir data\runs

This will:

-   Fetch weather data for selected cities
-   Compute distances to the reference city
-   Generate timestamped historical files
-   Update a latest snapshot file

Generated outputs:

    data/
    ├── latest_weather.json
    ├── latest_weather.csv
    └── runs/
        ├── 2026-02-23_11-32-01_weather.csv
        ├── 2026-02-23_12-32-01_weather.csv
        └── ...

Each execution produces a new historical snapshot.

------------------------------------------------------------------------

## Exploratory Data Analysis

Open:

    notebooks/Weather_Analysis_Portfolio.ipynb

The notebook:

-   Loads historical data
-   Reconstructs timestamps
-   Performs:
    -   Temperature evolution analysis
    -   Average temperature analysis
    -   Correlation analysis
    -   Humidity evolution
    -   Geographic visualization using Folium

The notebook maintains the academic analytical structure while using the
improved pipeline outputs.

------------------------------------------------------------------------

## Technical Design

The project follows a clear separation of concerns:

-   `pipeline.py` → extraction and transformation logic
-   `run_pipeline.py` → execution interface
-   `notebook` → analysis layer
-   `.env` → secure configuration
-   `data/runs` → historical storage

This structure makes the project:

-   Reproducible
-   Modular
-   Automation-ready
-   Easy to extend

------------------------------------------------------------------------

## Possible Extensions

Future improvements could include:

-   Database storage (PostgreSQL)
-   Docker containerization
-   Automated scheduling
-   Cloud deployment
-   CI/CD pipeline
-   Unit testing
-   Data validation layer

------------------------------------------------------------------------

## Academic Context

Originally developed for:

Master's Degree in Business Intelligence and Analytics\
Instituto Politécnico de Tomar

Refactored for portfolio presentation and professional best practices.

------------------------------------------------------------------------

## Author

Soraia Pedro Tarrinha\
Backend Developer \| Python & Data\
Portugal
