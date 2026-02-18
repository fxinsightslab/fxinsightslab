# RL開発計画に基づくFX取引システム（プロトタイプ）

このディレクトリは、強化学習（RL）でFX売買ロジックを検証するための最小実装です。

## 構成

- `plan.md`: RL開発計画（段階・KPI・リスク管理）
- `src/fx_rl/data.py`: 価格データの読み込み・特徴量生成
- `src/fx_rl/env.py`: FX売買環境（離散行動: Hold/Buy/Sell）
- `src/fx_rl/agent.py`: 離散化状態向けQ-Learningエージェント
- `src/fx_rl/train.py`: 学習実行スクリプト
- `src/fx_rl/backtest.py`: 学習済みQテーブルでのバックテスト
- `tests/test_env.py`: 環境と学習器の基本テスト

## 実行方法

```bash
cd rl_fx_system
python -m src.fx_rl.train
python -m src.fx_rl.backtest
python -m unittest discover -s tests
```

## 補足

- 実運用向けではなく、**研究・検証用**です。
- 実際の発注機能（ブローカーAPI接続）は含みません。
