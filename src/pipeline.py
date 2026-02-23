import os
from datetime import datetime
import pandas as pd
from geopy.distance import geodesic
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_api_key() -> str:
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        raise RuntimeError("Missing OPENWEATHER_API_KEY. Create a .env file in the project root.")
    return key

def fetch_weather(city: str) -> dict:
    params = {"q": city, "appid": get_api_key(), "units": "metric"}
    r = requests.get(BASE_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def extract_city_record(payload: dict) -> dict:
    return {
        "city": payload.get("name"),
        "country": payload.get("sys", {}).get("country"),
        "lat": payload.get("coord", {}).get("lat"),
        "lon": payload.get("coord", {}).get("lon"),
        "temp_c": payload.get("main", {}).get("temp"),
        "humidity": payload.get("main", {}).get("humidity"),
        "pressure": payload.get("main", {}).get("pressure"),
        "weather_main": (payload.get("weather") or [{}])[0].get("main"),
        "weather_desc": (payload.get("weather") or [{}])[0].get("description"),
        "wind_speed": payload.get("wind", {}).get("speed"),
        "wind_deg": payload.get("wind", {}).get("deg"),
    }

def add_distance_km(df: pd.DataFrame, ref_city: str) -> pd.DataFrame:
    ref_payload = fetch_weather(ref_city)
    ref = extract_city_record(ref_payload)

    if ref["lat"] is None or ref["lon"] is None:
        raise RuntimeError(f"Could not get coordinates for reference city: {ref_city}")

    ref_point = (ref["lat"], ref["lon"])

    def compute(row):
        if pd.isna(row["lat"]) or pd.isna(row["lon"]):
            return None
        return float(geodesic(ref_point, (row["lat"], row["lon"])).km)

    df["distance_to_ref_km"] = df.apply(compute, axis=1)
    df["ref_city"] = ref_city
    return df

def write_outputs(df: pd.DataFrame, out_json_path: str | None = None, out_dir: str = "data/runs") -> str:
    # If out_json_path is not given, create a timestamped file inside out_dir
    if out_json_path is None:
        os.makedirs(out_dir, exist_ok=True)
        run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        out_json_path = os.path.join(out_dir, f"{run_id}_weather.json")
    else:
        os.makedirs(os.path.dirname(out_json_path), exist_ok=True)

    # Write JSON + CSV for the run
    df.to_json(out_json_path, orient="records", indent=2)
    out_csv_path = os.path.splitext(out_json_path)[0] + ".csv"
    df.to_csv(out_csv_path, index=False)

    # Also keep a "latest" snapshot for notebooks
    latest_json = os.path.join("data", "latest_weather.json")
    latest_csv = os.path.join("data", "latest_weather.csv")
    os.makedirs("data", exist_ok=True)
    df.to_json(latest_json, orient="records", indent=2)
    df.to_csv(latest_csv, index=False)

    return out_json_path

def run_pipeline(ref_city: str, cities: list[str], out_path: str | None = None, out_dir: str = "data/runs"):
    records = []
    for city in cities:
        payload = fetch_weather(city)
        records.append(extract_city_record(payload))

    df = pd.DataFrame(records)
    df = add_distance_km(df, ref_city=ref_city)

    saved_path = write_outputs(df, out_json_path=out_path, out_dir=out_dir)
    return df, saved_path
