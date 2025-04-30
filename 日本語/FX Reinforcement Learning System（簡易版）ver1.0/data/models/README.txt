モデルバックアップ用ファイル

このファイルは、学習モデルを誤って上書き保存してしまった場合に備えて、
重要なモデルデータを安全に保存しておくために使用します。

✅ 運用ルール：
- 新しい学習開始前に、必ず直近モデルをこのバックアップにコピーしてください。
- バックアップから復元する場合は、手動で対象ファイルをコピーして戻してください。
- 本バックアップは自動では更新されません。重要なタイミングで必ず手動保存してください。

❗注意：
- バックアップが存在しない場合、復元はできません。
- 上書きに備えて定期的にバックアップを取る習慣をつけてください。

※　PPO学習ログの具体的な確認方法は別添の”PPO学習ログの具体的な確認方法”をご確認ください。


以下に学習終了時のそれぞれのPPOの学習成績（学習ログ）を載せます。

#############
# Trend　AI #
#############
------------------------------------------
| rollout/                |              |
|    ep_len_mean          | 9.95e+03     |
|    ep_rew_mean          | 325          |
| time/                   |              |
|    fps                  | 380          |
|    iterations           | 49           |
|    time_elapsed         | 263          |
|    total_timesteps      | 100352       |
| train/                  |              |
|    approx_kl            | 0.0026731002 |
|    clip_fraction        | 0.0172       |
|    clip_range           | 0.2          |
|    entropy_loss         | -0.264       |
|    explained_variance   | 0.616        |
|    learning_rate        | 0.0003       |
|    loss                 | 24.2         |
|    n_updates            | 1460         |
|    policy_gradient_loss | -0.00204     |
|    value_loss           | 67.8         |
------------------------------------------

##################
# Volatility　AI #
##################

------------------------------------------
| rollout/                |              |
|    ep_len_mean          | 9.95e+03     |
|    ep_rew_mean          | 723          |
| time/                   |              |
|    fps                  | 271          |
|    iterations           | 49           |
|    time_elapsed         | 369          |
|    total_timesteps      | 100352       |
| train/                  |              |
|    approx_kl            | 0.0053420793 |
|    clip_fraction        | 0.0313       |
|    clip_range           | 0.2          |
|    entropy_loss         | -0.391       |
|    explained_variance   | 0.862        |
|    learning_rate        | 0.0003       |
|    loss                 | 0.0463       |
|    n_updates            | 1120         |
|    policy_gradient_loss | -0.0033      |
|    value_loss           | 0.153        |
------------------------------------------


##############
# Manager_AI #
##############

-----------------------------------------
| rollout/                |             |
|    ep_len_mean          | 9.95e+03    |
|    ep_rew_mean          | -39.4       |
| time/                   |             |
|    fps                  | 191         |
|    iterations           | 2442        |
|    time_elapsed         | 26110       |
|    total_timesteps      | 5001216     |
| train/                  |             |
|    approx_kl            | 0.008707308 |
|    clip_fraction        | 0.0353      |
|    clip_range           | 0.2         |
|    entropy_loss         | -0.12       |
|    explained_variance   | 0.371       |
|    learning_rate        | 0.0003      |
|    loss                 | -0.0109     |
|    n_updates            | 35680       |
|    policy_gradient_loss | -0.0077     |
|    value_loss           | 0.0084      |
-----------------------------------------