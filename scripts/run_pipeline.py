import argparse
from src.pipeline import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="Weather Data Pipeline")
    parser.add_argument("--ref-city", required=True, help="Reference city (e.g., Peniche)")
    parser.add_argument("--cities", nargs="+", required=True, help="Cities list (e.g., Tomar Coimbra Braga)")
    parser.add_argument("--out", default=None, help="Optional: fixed output JSON path")
    parser.add_argument("--out-dir", default="data/runs", help="Folder for timestamped runs")
    args = parser.parse_args()

    _, saved_path = run_pipeline(
        ref_city=args.ref_city,
        cities=args.cities,
        out_path=args.out,
        out_dir=args.out_dir
    )

    print(f"Saved run to: {saved_path}")
    print("Updated: data/latest_weather.json and data/latest_weather.csv")

if __name__ == "__main__":
    main()
