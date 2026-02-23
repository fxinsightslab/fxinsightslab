import logging

import pandas as pd

logger = logging.getLogger(__name__)


def check_tz(df: pd.DataFrame) -> None:
    """ts_utc列がtz-aware UTCであることを検証する。"""
    if "ts_utc" not in df.columns:
        message = "missing ts_utc column"
        logger.error(message)
        raise ValueError(message)
    if df["ts_utc"].dt.tz is None:
        message = "ts_utc must be timezone-aware"
        logger.error(message)
        raise ValueError(message)
    if str(df["ts_utc"].dt.tz) != "UTC":
        message = "ts_utc must be UTC timezone"
        logger.error(message)
        raise ValueError(message)


def check_missing(df: pd.DataFrame) -> None:
    """必須列の欠損値を検証する。"""
    required = ["symbol", "ts_utc", "o", "h", "l", "c", "v", "spread"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        message = f"missing required columns: {', '.join(missing)}"
        logger.error(message)
        raise ValueError(message)

    null_counts = df[required].isnull().sum()
    null_columns = [col for col, cnt in null_counts.items() if cnt > 0]
    if null_columns:
        message = f"null values detected in columns: {', '.join(null_columns)}"
        logger.error(message)
        raise ValueError(message)
