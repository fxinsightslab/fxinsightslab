from pathlib import Path

import pandas as pd

from fxai.io.load_mt5 import load_mt5


def load_prices_csv(path: str | Path, symbol: str) -> pd.DataFrame:
    """後方互換: CSV読み込みをload_mt5へ委譲する。"""
    return load_mt5(symbol=symbol, timeframe="M1", input_path=path)
