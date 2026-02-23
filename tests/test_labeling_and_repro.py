import hashlib
from pathlib import Path

import pandas as pd

from fxai.features.make_features import make
from fxai.features.regime import classify
from fxai.io.load_mt5 import load_mt5
from fxai.labeling.triple_barrier import triple_barrier
from fxai.resample.ohlc import ohlc


FIXTURE_DIR = Path("tests/fixtures")


def _hash_df(df: pd.DataFrame) -> str:
    return hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()


def test_triple_barrier_shape() -> None:
    close = pd.Series([100, 101, 102, 101, 100], dtype="float64")
    atr = pd.Series([0.5, 0.5, 0.5, 0.5, 0.5], dtype="float64")
    labels = triple_barrier(close, atr, k_up=2.0, k_dn=2.0, n_bars=2)

    assert labels.shape == (5, 5)
    assert set(labels.columns) == {
        "label_direction",
        "label_success",
        "label_t_bar",
        "label_up_bar",
        "label_down_bar",
    }


def test_reproducible_pipeline_hash() -> None:
    m1 = load_mt5("USDJPY", "M1", FIXTURE_DIR / "m1_10rows.csv")
    bars = ohlc(m1, rule="M5", drop_incomplete=True)
    feat = make(bars, cfg={"return_window": 1, "vol_window": 2, "z_window": 2})
    feat["regime"] = classify(feat)
    atr = (feat["h"] - feat["l"]).rolling(2, min_periods=1).mean()
    labels = triple_barrier(feat["c"], atr, k_up=1.5, k_dn=1.5, n_bars=2)

    out1 = pd.concat([feat, labels], axis=1)
    out2 = pd.concat([feat.copy(), labels.copy()], axis=1)

    assert _hash_df(out1) == _hash_df(out2)
