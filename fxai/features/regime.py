import pandas as pd


def classify(df_feat: pd.DataFrame) -> pd.Series:
    """特徴量から簡易regimeラベルを返す。"""
    trend = df_feat["ret_1"].abs() > df_feat["ret_1"].rolling(20, min_periods=20).std()
    highvol = df_feat["volatility"] > df_feat["volatility"].rolling(20, min_periods=20).median()

    regime = pd.Series("range", index=df_feat.index, dtype="string")
    regime[trend & ~highvol] = "trend"
    regime[trend & highvol] = "highvol"
    regime[~trend & highvol] = "news"
    return regime
