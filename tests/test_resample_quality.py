from pathlib import Path

import pandas as pd
import pytest

from fxai.io.load_mt5 import load_mt5
from fxai.resample.ohlc import ohlc
from fxai.resample.quality import check_missing


FIXTURE_DIR = Path("tests/fixtures")


def test_resample_m5_aggregation_matches_contract() -> None:
    df = load_mt5("USDJPY", "M1", FIXTURE_DIR / "m1_10rows.csv")
    out = ohlc(df, rule="M5", drop_incomplete=True)

    assert len(out) == 2
    first = out.iloc[0]
    assert first["o"] == 100
    assert first["h"] == 101.6
    assert first["l"] == 99
    assert first["c"] == 101.5
    assert first["v"] == 50


def test_check_missing_fails_on_null() -> None:
    df = pd.DataFrame(
        {
            "symbol": ["USDJPY"],
            "ts_utc": [pd.Timestamp("2026-01-01T00:00:00+00:00")],
            "o": [1.0],
            "h": [1.1],
            "l": [0.9],
            "c": [None],
            "v": [10],
            "spread": [0.2],
        }
    )
    with pytest.raises(ValueError, match="null values detected"):
        check_missing(df)
