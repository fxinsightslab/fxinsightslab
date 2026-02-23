from pathlib import Path

import pandas as pd
import pytest

from fxai.io.load_prices import load_prices_csv


FIXTURE_DIR = Path("tests/fixtures")


def test_load_prices_csv_success_creates_utc_and_columns() -> None:
    df = load_prices_csv(FIXTURE_DIR / "load_prices_valid.csv", symbol="USDJPY")

    assert list(df.columns) == ["symbol", "ts_utc", "o", "h", "l", "c", "v", "spread"]
    assert (df["symbol"] == "USDJPY").all()
    assert str(df["ts_utc"].dt.tz) == "UTC"
    assert df["ts_utc"].is_monotonic_increasing
    assert pd.api.types.is_numeric_dtype(df["o"])
    assert pd.api.types.is_numeric_dtype(df["h"])
    assert pd.api.types.is_numeric_dtype(df["l"])
    assert pd.api.types.is_numeric_dtype(df["c"])
    assert pd.api.types.is_numeric_dtype(df["v"])
    assert pd.api.types.is_numeric_dtype(df["spread"])


def test_load_prices_csv_fails_on_naive_ts() -> None:
    with pytest.raises(ValueError, match="tz-aware"):
        load_prices_csv(FIXTURE_DIR / "load_prices_naive_ts.csv", symbol="USDJPY")


def test_load_prices_csv_fails_on_numeric_conversion_error() -> None:
    with pytest.raises(ValueError, match="numeric conversion failed"):
        load_prices_csv(FIXTURE_DIR / "load_prices_bad_numeric.csv", symbol="USDJPY")


def test_load_prices_csv_fails_on_duplicate_ts_utc() -> None:
    with pytest.raises(ValueError, match="duplicate ts_utc") as exc_info:
        load_prices_csv(FIXTURE_DIR / "load_prices_duplicate_ts.csv", symbol="USDJPY")

    assert "Mixed timezones" not in str(exc_info.value)


def test_load_prices_csv_success_with_mixed_offsets() -> None:
    df = load_prices_csv(FIXTURE_DIR / "load_prices_mixed_offsets_valid.csv", symbol="USDJPY")

    assert str(df["ts_utc"].dt.tz) == "UTC"
    assert str(df["ts_utc"].dtype) == "datetime64[ns, UTC]"
    assert df["ts_utc"].is_monotonic_increasing
