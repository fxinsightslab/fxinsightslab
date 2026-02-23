# AGENTS.md（Codex作業規約 / 必須）
更新日: 2026-02-18（JST）

このリポジトリでは、AI実装（Codex等）が**迷わず正しい差分**を出すために、以下を厳守する。

---

## 0. 最優先原則（破るとPRは即FAIL）
1) **テストでDoDを証明する**（pytest必須）
2) **再現性**：同一入力→同一出力（sha256で検証可能）
3) **Data Contract厳守**：TZ/欠損/スキーマ/リサンプル定義を勝手に変えない
4) **曖昧禁止**：例外時のエラーメッセージで原因が一意に分かること

---

## 1. コーディング規約
- **print禁止**：loggingのみ
- **コメントは日本語**（必要十分。長文は避ける）
- **例外は握りつぶさない**：raiseしてFAIL（原因メッセージ必須）
- 関数は小さく、責務は1つ
- 依存追加は最小（pandas / pyarrow / pytest を想定）
  - 追加したい場合は「なぜ必要か」をPR本文に1行で書く

---

## 2. Data Contract（絶対）
- 入力時刻は **tz-aware必須**（naiveはFAIL）
- 内部基準時刻は **UTCの ts_utc 列**のみ
- **欠損を埋めない**（ffill/bfill禁止）
- リサンプル定義：
  - open=first, high=max, low=min, close=last, volume=sum
  - spread（暫定）= mean（後で仕様変更可。ただし勝手に変えない）
- `drop_incomplete=True` の時は **末尾の未完バーを必ず破棄**

---

## 3. テスト規約（pytest）
- fixturesは `tests/fixtures/` に置く
- 期待値が明確な「小さな固定データ」を使う（数行で良い）
- テストは以下を含める：
  - 正常系（期待OHLC一致）
  - 異常系（naive ts / 数値変換失敗 / 重複ts / 欠損）でFAILすること

---

## 4. ログ規約
- `logger = logging.getLogger(__name__)`
- 例外の前に「何が違反か」をlogger.errorで出してよい（ただし情報過多は禁止）
- ただし、テストのFAILは例外で担保すること

---

## 5. 実行コマンド（最低限）
- 単体テスト: `python -m pytest -q`
- 追加で必要なコマンドがあれば `RUN_COMMANDS.txt` に追記する

---

## 6. PRの提出形式（Codex向け）
PR本文には必ず以下を書く：
- 実装したIssue番号
- 変更ファイル一覧
- DoDの満たし方（どのテストで証明したか）
