# BACKLOG.md（W1–W2：土台・データ契約パック）
更新日: 2026-02-18（JST）

目的：W1–W2の間に「データ契約（TZ/欠損/スキーマ/リサンプル）」をコードとテストで固定し、
以後の検証が崩壊しない土台を作る。

---

## Issue 001: Data Contract 文書化（憲法の明文化）
### Goal
- Data Contractを1ファイルに明文化し、以後の実装が迷わない状態にする。

### Scope（変更対象）
- `docs/DATA_CONTRACT.md`（新規）

### Requirements
- スキーマ（最低限）：`symbol, ts_utc, o, h, l, c, v, spread`
- TZ規約：入力tz-aware必須、内部はUTC（ts_utc）
- 欠損規約：ffill/bfill禁止、欠損は破棄 or 欠損フラグ化（W1は破棄推奨）
- Resample定義：open=first, high=max, low=min, close=last, v=sum, spread=mean（暫定）
- `drop_incomplete` の定義：末尾未完バー破棄
- Quality Gateの最低条件（単調性、重複禁止、欠損率など）
- 禁止事項一覧（ffill、naive ts、暗黙TZ変換、未来参照 など）

### DoD
- この1ファイルだけで、W1–W2の実装前提が読める

### Test
- なし（ドキュメント）

---

## Issue 002: Loader（TZ強制 + 数値強制 + 重複禁止）
### Goal
- 入口でデータの不正を落とし、以後の処理が“静かに壊れない”ようにする。

### Scope
- `fxai/io/load_prices.py`（新規）
- `tests/test_load_prices.py`（新規）
- `tests/fixtures/`（サンプルCSV追加）

### Requirements
- 入力CSVを読み、`o,h,l,c,v,spread` を数値変換（失敗は例外）
- `ts` が tz-aware でなければ例外（naiveはFAIL）
- `ts_utc` 列を作り、UTCへ正規化
- `ts_utc` の重複は禁止（例外）
- 並びは `ts_utc` 昇順に整列

### DoD
- 正常系：fixtureを読み込み、`ts_utc` がUTCであること、数値列がfloat/intであること
- 異常系：naive ts / 数値文字列混入 / 重複ts でFAILするテストがある

### Commands
- `python -m pytest -q`

---

## Issue 003: Resample（厳密OHLCV + drop_incomplete）
### Goal
- M1→M5/H1/H4 の厳密リサンプリングを固定し、出力が期待値と一致することをテストで保証する。

### Scope
- `fxai/resample/ohlc.py`（新規）
- `tests/test_resample_ohlc.py`（新規）

### Requirements
- 入力は `ts_utc`（UTC）を前提
- 集約：open=first, high=max, low=min, close=last, v=sum, spread=mean
- `drop_incomplete=True` の場合、末尾の未完バーを必ず捨てる
- 欠損を埋めない（ffill禁止）

### DoD
- 固定入力（数分分のM1）に対して、M5集約結果が期待OHLCVと完全一致
- `drop_incomplete` の挙動がテストで固定されている

### Commands
- `python -m pytest -q`

---

## Issue 004: Quality Gate（品質検査）
### Goal
- データ品質の最低条件をコードで強制し、NGなら“どのルール違反か”を一意に示してFAILさせる。

### Scope
- `fxai/resample/quality.py`（新規）
- `tests/test_quality.py`（新規）

### Checks（最低限）
- `ts_utc` 単調増加、重複0
- 欠損率（列別/期間別）
- 異常値（high < low、負volume 等）
- 週末/休場の穴の扱い（許容範囲は docs/DATA_CONTRACT.md に従う）

### DoD
- 代表的な違反でFAILするテストがある（メッセージが一意）

### Commands
- `python -m pytest -q`

---

## Issue 005: Manifest（sha256でbit一致検証）
### Goal
- 入出力成果物のハッシュを固定し、同一入力→同一出力が検証できる状態にする。

### Scope
- `fxai/ops/manifest.py`（新規）
- `tests/test_manifest.py`（新規）
- `RUN_COMMANDS.txt`（更新）

### Requirements
- 指定ディレクトリ配下のファイル一覧とsha256をJSONで出力
- 生成物の順序は安定（ソート固定）
- 例外時は原因が一意に分かる

### DoD
- 小さなfixtureファイル群で、期待sha256と一致するテストがある

### Commands
- `python -m pytest -q`
