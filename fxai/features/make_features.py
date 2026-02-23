import pandas as pd


def make(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """基本特徴量を生成する。"""
    out = df.copy()
    ret_window = int(cfg.get("return_window", 1))
    vol_window = int(cfg.get("vol_window", 12))
    z_window = int(cfg.get("z_window", 20))

    out["ret_1"] = out["c"].pct_change(ret_window)
    out["range_hl"] = (out["h"] - out["l"]) / out["c"].replace(0, pd.NA)
    out["spread_ratio"] = out["spread"] / out["c"].replace(0, pd.NA)
    out["volatility"] = out["ret_1"].rolling(vol_window, min_periods=vol_window).std()
    ma = out["c"].rolling(z_window, min_periods=z_window).mean()
    sd = out["c"].rolling(z_window, min_periods=z_window).std()
    out["zscore_close"] = (out["c"] - ma) / sd.replace(0, pd.NA)

    return out
