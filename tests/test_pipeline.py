"""Offline tests: no live API key or network required."""
import pandas as pd
import pytest
from src import pipeline

def weather(city, lat, lon):
    return {
        "name": city, "sys": {"country": "PT"},
        "coord": {"lat": lat, "lon": lon},
        "main": {"temp": 15.0, "humidity": 70, "pressure": 1015},
        "weather": [{"main": "Clear", "description": "clear sky"}],
        "wind": {"speed": 2.5, "deg": 180},
    }

def test_pipeline_creates_latest_and_history(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake-key-for-offline-tests")
    seen = []
    class FakeResponse:
        def __init__(self, payload): self.payload = payload
        def raise_for_status(self): pass
        def json(self): return self.payload
    def fake_get(url, params, timeout):
        seen.append(params["q"])
        city = params["q"].split(",")[0]
        return FakeResponse({
            "Peniche": weather("Peniche", 39.36, -9.38),
            "Beja": weather("Beja", 38.02, -7.86),
            "Tomar": weather("Tomar", 39.60, -8.41),
        }[city])
    monkeypatch.setattr(pipeline.requests, "get", fake_get)
    result, saved = pipeline.run_pipeline("Peniche", ["Beja", "Tomar"])
    assert seen == ["Beja,PT", "Tomar,PT", "Peniche,PT"]
    assert len(result) == 2
    assert (tmp_path / saved).exists()
    assert (tmp_path / "data/latest_weather.csv").exists()
    current = pd.read_csv("data/latest_weather.csv")
    assert set(current.city) == {"Beja", "Tomar"}
    assert 0 < current.loc[current.city == "Beja", "distance_to_ref_km"].iloc[0] < 300
    assert "collected_at_utc" in current

def test_explicit_output_without_parent_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    saved = pipeline.write_outputs(pd.DataFrame({"city": ["Tomar"]}), "weather.json")
    assert saved == "weather.json"
    assert (tmp_path / "weather.csv").exists()

def test_empty_cities_rejected():
    with pytest.raises(ValueError, match="at least one"):
        pipeline.run_pipeline("Peniche", [])

def test_country_validation(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake-key-for-offline-tests")
    class FakeResponse:
        def raise_for_status(self): pass
        def json(self): return {"sys": {"country": "TN"}}
    monkeypatch.setattr(pipeline.requests, "get", lambda *a, **kw: FakeResponse())
    with pytest.raises(ValueError, match="non-PT"):
        pipeline.fetch_weather("Beja")
