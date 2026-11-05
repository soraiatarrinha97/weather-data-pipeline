"""Extra offline tests for failure paths and incomplete API data.

No actual API requests or secrets are used by these tests.
"""
import pandas as pd
import pytest
import requests

from src import pipeline


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="Missing OPENWEATHER_API_KEY"):
        pipeline.get_api_key()


@pytest.mark.parametrize("http_status", [401, 500])
def test_api_http_errors_are_propagated(monkeypatch, http_status):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "offline-test-only")
    class FakeResponse:
        def raise_for_status(self):
            raise requests.HTTPError(f"HTTP {http_status}")
    def fake_get(url, params, timeout):
        assert params["q"] == "Tomar,PT"
        assert timeout > 0
        return FakeResponse()
    monkeypatch.setattr(pipeline.requests, "get", fake_get)
    with pytest.raises(requests.HTTPError, match=str(http_status)):
        pipeline.fetch_weather("Tomar")


def test_missing_reference_coordinates_is_rejected(monkeypatch):
    monkeypatch.setattr(
        pipeline,
        "fetch_weather",
        lambda city: {"name": city, "sys": {"country": "PT"}, "coord": {}},
    )
    df = pd.DataFrame({"city": ["Tomar"], "lat": [39.6], "lon": [-8.4]})
    with pytest.raises(RuntimeError, match="No coordinates found"):
        pipeline.add_distance_km(df, "Peniche")


def test_missing_target_coordinates_produce_nan(monkeypatch):
    monkeypatch.setattr(
        pipeline,
        "fetch_weather",
        lambda city: {"name": city, "sys": {"country": "PT"}, "coord": {"lat": 39.36, "lon": -9.38}},
    )
    df = pd.DataFrame({"city": ["Tomar"], "lat": [None], "lon": [None]})
    result = pipeline.add_distance_km(df, "Peniche")
    assert pd.isna(result.loc[0, "distance_to_ref_km"])
    assert result.loc[0, "ref_city"] == "Peniche"
