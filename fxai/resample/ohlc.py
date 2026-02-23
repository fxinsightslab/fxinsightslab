import logging

import pandas as pd

from fxai.resample.quality import check_missing, check_tz

logger = logging.getLogger(__name__)


RULE_MAP = {"M5": "5min", "H1": "1h", "H4": "4h"}


def ohlc(df_m1: pd.DataFrame, rule: str, drop_incomplete: bool = True) -> pd.DataFrame:
    """M1データを契約定義のOHLCへ厳密集約する。"""
    check_tz(df_m1)
    check_missing(df_m1)
    if rule not in RULE_MAP:
        message = f"unsupported rule: {rule}"
        logger.error(message)
        raise ValueError(message)

    expected_freq = pd.Timedelta(minutes=1)
    diffs = df_m1["ts_utc"].sort_values().diff().dropna()
    if not diffs.empty and (diffs != expected_freq).any():
        message = "input ts_utc is not continuous M1 sequence"
        logger.error(message)
        raise ValueError(message)

    indexed = df_m1.sort_values("ts_utc", kind="mergesort").set_index("ts_utc")
    agg = (
        indexed.resample(RULE_MAP[rule], label="right", closed="left")
        .agg(
            {
                "symbol": "last",
                "o": "first",
                "h": "max",
                "l": "min",
                "c": "last",
                "v": "sum",
                "spread": "mean",
                "session": "last",
            }
        )
        .dropna(subset=["o", "h", "l", "c"])
        .reset_index()
    )

    if drop_incomplete and not agg.empty:
        expected = int(pd.Timedelta(RULE_MAP[rule]) / pd.Timedelta(minutes=1))
        counts = indexed["c"].resample(RULE_MAP[rule], label="right", closed="left").count().reset_index(drop=True)
        agg = agg.loc[counts == expected].reset_index(drop=True)

    return agg[["symbol", "ts_utc", "o", "h", "l", "c", "v", "spread", "session"]]
