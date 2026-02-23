import pandas as pd


def sharpe(returns: pd.Series, annualization: int = 252) -> float:
    """簡易Sharpeを計算する。"""
    std = returns.std()
    if std == 0 or pd.isna(std):
        return 0.0
    return float((returns.mean() / std) * (annualization ** 0.5))
