import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from fxai.features.make_features import make
from fxai.features.regime import classify
from fxai.io.load_mt5 import load_mt5
from fxai.io.parquet import from_parquet, to_parquet
from fxai.io.sqlite import sqlite_upsert
from fxai.labeling.triple_barrier import triple_barrier
from fxai.ops.logging import setup_logging
from fxai.resample.ohlc import ohlc
from fxai.resample.quality import check_missing, check_tz


def _hash_dataframe(df: pd.DataFrame) -> str:
    """DataFrameの再現性ハッシュを返す。"""
    csv_text = df.to_csv(index=False)
    return hashlib.sha256(csv_text.encode("utf-8")).hexdigest()




def _load_feature_config(path: str) -> dict:
    """最小YAML形式の特徴量設定を読み込む。"""
    cfg = {"return_window": 1, "vol_window": 12, "z_window": 20}
    text = Path(path).read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.endswith(":"):
            continue
        if ":" not in stripped:
            continue
        key, val = [x.strip() for x in stripped.split(":", 1)]
        if key in cfg:
            cfg[key] = int(val)
    return cfg


def cmd_ingest(args: argparse.Namespace) -> None:
    """取り込み処理を実行する。"""
    df = load_mt5(symbol=args.symbol, timeframe=args.timeframe, input_path=args.input)
    check_tz(df)
    check_missing(df)
    out_dir = Path(args.out)
    out_path = out_dir / f"{args.symbol}_{args.timeframe}.parquet"
    to_parquet(df, out_path)
    sqlite_upsert("ingest_meta", pd.DataFrame([{"path": str(out_path), "sha256": _hash_dataframe(df)}]), out_dir / "meta.db")


def cmd_resample(args: argparse.Namespace) -> None:
    """リサンプル処理を実行する。"""
    src_path = Path(args.input) / f"{args.symbol}_{args.timeframe}.parquet"
    raw_df = from_parquet(src_path)
    out_dir = Path(args.out)
    for rule in args.rules.split(","):
        bar = ohlc(raw_df, rule=rule, drop_incomplete=True)
        out_path = out_dir / f"{args.symbol}_{rule}.parquet"
        to_parquet(bar, out_path)


def cmd_features(args: argparse.Namespace) -> None:
    """特徴量生成を実行する。"""
    cfg = _load_feature_config(args.config)
    src_path = Path(args.input) / f"{args.symbol}_{args.rule}.parquet"
    df = from_parquet(src_path)
    feat = make(df, cfg=cfg)
    feat["regime"] = classify(feat)
    out_path = Path(args.out) / f"{args.symbol}_{args.rule}_features.parquet"
    to_parquet(feat, out_path)


def cmd_label(args: argparse.Namespace) -> None:
    """ラベル生成を実行する。"""
    src_path = Path(args.input) / f"{args.symbol}_{args.rule}_features.parquet"
    df = from_parquet(src_path)
    atr = (df["h"] - df["l"]).rolling(14, min_periods=1).mean()
    labels = triple_barrier(
        close=df["c"],
        atr=atr,
        k_up=args.k_up,
        k_dn=args.k_dn,
        n_bars=args.n_bars,
        event_window=args.event_window,
    )
    out = pd.concat([df, labels], axis=1)
    out_path = Path(args.out) / f"{args.symbol}_{args.rule}_labels.parquet"
    to_parquet(out, out_path)
    hash_path = Path(args.out) / f"{args.symbol}_{args.rule}_labels.sha256"
    hash_path.parent.mkdir(parents=True, exist_ok=True)
    hash_path.write_text(json.dumps({"sha256": _hash_dataframe(out)}), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    """CLIパーサーを構築する。"""
    parser = argparse.ArgumentParser(prog="fxai.cli")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest")
    ingest.add_argument("--input", required=True)
    ingest.add_argument("--symbol", required=True)
    ingest.add_argument("--timeframe", default="M1")
    ingest.add_argument("--out", required=True)
    ingest.set_defaults(func=cmd_ingest)

    res = sub.add_parser("resample")
    res.add_argument("--input", required=True)
    res.add_argument("--symbol", required=True)
    res.add_argument("--timeframe", default="M1")
    res.add_argument("--out", required=True)
    res.add_argument("--rules", required=True)
    res.set_defaults(func=cmd_resample)

    feat = sub.add_parser("features")
    feat.add_argument("--input", required=True)
    feat.add_argument("--symbol", required=True)
    feat.add_argument("--rule", default="M5")
    feat.add_argument("--out", required=True)
    feat.add_argument("--config", default="fxai/ops/config.yaml")
    feat.set_defaults(func=cmd_features)

    label = sub.add_parser("label")
    label.add_argument("--input", required=True)
    label.add_argument("--symbol", required=True)
    label.add_argument("--rule", default="M5")
    label.add_argument("--out", required=True)
    label.add_argument("--k_up", type=float, required=True)
    label.add_argument("--k_dn", type=float, required=True)
    label.add_argument("--n_bars", type=int, required=True)
    label.add_argument("--event_window", type=int)
    label.set_defaults(func=cmd_label)

    return parser


def main() -> None:
    """CLIエントリポイント。"""
    setup_logging()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
