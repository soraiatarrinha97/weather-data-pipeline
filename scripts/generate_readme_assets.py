"""Generate portfolio screenshots from the included historical observations.

Run from the repository root:
    .\.venv\Scripts\python.exe scripts/generate_readme_assets.py

The dataset is historical (2021-2022), not a current forecast.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "sample_data" / "historic_weather_2021_2022.csv"
ASSETS = ROOT / "assets"


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_FILE)
    df["date_time"] = pd.to_datetime(df["Timestamp"], dayfirst=True, errors="raise")
    cities = ["Peniche", "Tomar", "Coimbra", "Beja"]

    # Time series: 6-hour averages provide a readable view across six days.
    fig, ax = plt.subplots(figsize=(10.5, 4.5))
    for city in cities:
        city_df = df.loc[df["City"] == city].set_index("date_time").sort_index()
        samples = city_df["temp"].resample("6h").mean().dropna()
        ax.plot(samples.index, samples.values, marker=".", linewidth=1.7, label=city)
    ax.set(title="Temperature over time · selected cities", ylabel="Temperature (°C)", xlabel="December 2021 – January 2022")
    ax.grid(alpha=0.22)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.20), frameon=False)
    fig.autofmt_xdate(rotation=0)
    fig.tight_layout()
    fig.savefig(ASSETS / "temperature_timeseries.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    # Historical observations: 11 cities, sorted for easy comparison.
    mean_humidity = df.groupby("City", as_index=True)["humidity"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    bars = ax.barh(mean_humidity.index, mean_humidity.values)
    ax.set(title="Average relative humidity · 11 cities", xlabel="Relative humidity (%)")
    ax.set_xlim(0, max(100, mean_humidity.max() + 9))
    ax.grid(axis="x", alpha=0.18)
    ax.set_axisbelow(True)
    for bar, value in zip(bars, mean_humidity.values):
        ax.text(value + 0.7, bar.get_y() + bar.get_height()/2, f"{value:.1f}%", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(ASSETS / "humidity_by_city.png", dpi=170, bbox_inches="tight")
    plt.close(fig)
    print("Generated assets/temperature_timeseries.png and assets/humidity_by_city.png")


if __name__ == "__main__":
    main()
