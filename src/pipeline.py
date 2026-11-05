"""Weather collection and snapshot persistence for the portfolio project."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from geopy.distance import geodesic

load_dotenv()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_api_key() -> str:
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        raise RuntimeError(
            "Missing OPENWEATHER_API_KEY. Create .env in the repository root "
            "(see .env.example), then rerun from the project root."
        )
    return key

def fetch_weather(city: str) -> dict:
    """Request a Portuguese municipality to prevent e.g. Beja (Tunisia)."""
    city_query = city if "," in city else f"{city},PT"
    response = requests.get(
        BASE_URL,
        params={"q": city_query, "appid": get_api_key(), "units": "metric"},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("sys", {}).get("country") != "PT":
        raise ValueError(f"OpenWeather returned a non-PT location for {city!r}")
    return payload

def extract_city_record(payload: dict) -> dict:
    weather = payload.get("weather") or [{}]
    return {
        "city": payload.get("name"),
        "country": payload.get("sys", {}).get("country"),
        "lat": payload.get("coord", {}).get("lat"),
        "lon": payload.get("coord", {}).get("lon"),
        "temp_c": payload.get("main", {}).get("temp"),
        "humidity": payload.get("main", {}).get("humidity"),
        "pressure": payload.get("main", {}).get("pressure"),
        "weather_main": weather[0].get("main"),
        "weather_desc": weather[0].get("description"),
        "wind_speed": payload.get("wind", {}).get("speed"),
        "wind_deg": payload.get("wind", {}).get("deg"),
    }

def add_distance_km(df: pd.DataFrame, ref_city: str) -> pd.DataFrame:
    ref = extract_city_record(fetch_weather(ref_city))
    if ref["lat"] is None or ref["lon"] is None:
        raise RuntimeError(f"No coordinates found for reference city: {ref_city}")
    ref_point = (ref["lat"], ref["lon"])
    result = df.copy()
    result["distance_to_ref_km"] = result.apply(
        lambda row: (
            float(geodesic(ref_point, (row["lat"], row["lon"])).km)
            if pd.notna(row["lat"]) and pd.notna(row["lon"]) else float("nan")
        ), axis=1,
    )
    result["ref_city"] = ref_city
    return result

def write_outputs(
    df: pd.DataFrame,
    out_json_path: str | None = None,
    out_dir: str = "data/runs",
) -> str:
    if out_json_path is None:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        json_path = Path(out_dir) / f"{run_id}_weather.json"
    else:
        json_path = Path(out_json_path)
        json_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_json(json_path, orient="records", indent=2)
    df.to_csv(json_path.with_suffix(".csv"), index=False)
    latest = Path("data")
    latest.mkdir(parents=True, exist_ok=True)
    df.to_json(latest / "latest_weather.json", orient="records", indent=2)
    df.to_csv(latest / "latest_weather.csv", index=False)
    return str(json_path)

def run_pipeline(
    ref_city: str,
    cities: list[str],
    out_path: str | None = None,
    out_dir: str = "data/runs",
) -> tuple[pd.DataFrame, str]:
    if not cities:
        raise ValueError("Select at least one city.")
    collected_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    records = [extract_city_record(fetch_weather(city)) for city in cities]
    df = pd.DataFrame(records)
    df["collected_at_utc"] = collected_at
    df = add_distance_km(df, ref_city=ref_city)
    saved = write_outputs(df, out_json_path=out_path, out_dir=out_dir)
    return df, saved
