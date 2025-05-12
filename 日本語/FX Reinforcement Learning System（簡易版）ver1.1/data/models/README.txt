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
----------------------------------------
| rollout/                |            |
|    ep_len_mean          | 99         |
|    ep_rew_mean          | 32.4       |
| time/                   |            |
|    fps                  | 197        |
|    iterations           | 49         |
|    time_elapsed         | 508        |
|    total_timesteps      | 100352     |
| train/                  |            |
|    approx_kl            | 0.01314174 |
|    clip_fraction        | 0.0644     |
|    clip_range           | 0.2        |
|    entropy_loss         | -0.262     |
|    explained_variance   | 0.994      |
|    learning_rate        | 0.0003     |
|    loss                 | 0.161      |
|    n_updates            | 3740       |
|    policy_gradient_loss | -0.00191   |
|    value_loss           | 0.953      |
----------------------------------------

##################
# Volatility　AI #
##################

-----------------------------------------
| rollout/                |             |
|    ep_len_mean          | 99          |
|    ep_rew_mean          | 4.25        |
| time/                   |             |
|    fps                  | 134         |
|    iterations           | 8           |
|    time_elapsed         | 122         |
|    total_timesteps      | 16384       |
| train/                  |             |
|    approx_kl            | 0.008185465 |
|    clip_fraction        | 0.0526      |
|    clip_range           | 0.2         |
|    entropy_loss         | -0.108      |
|    explained_variance   | 0.999       |
|    learning_rate        | 0.0003      |
|    loss                 | -0.00148    |
|    n_updates            | 1839        |
|    policy_gradient_loss | -0.00461    |
|    value_loss           | 0.000926    |
-----------------------------------------


##############
# Manager_AI #
##############

-------------------------------------------
| rollout/                |               |
|    ep_len_mean          | 99            |
|    ep_rew_mean          | -0.101        |
| time/                   |               |
|    fps                  | 149           |
|    iterations           | 91            |
|    time_elapsed         | 1244          |
|    total_timesteps      | 186368        |
| train/                  |               |
|    approx_kl            | 3.2761425e-05 |
|    clip_fraction        | 0.000391      |
|    clip_range           | 0.2           |
|    entropy_loss         | -0.00277      |
|    explained_variance   | 0.961         |
|    learning_rate        | 5.31e-05      |
|    loss                 | 6.06e-06      |
|    n_updates            | 3840          |
|    policy_gradient_loss | -0.000548     |
|    value_loss           | 1.26e-05      |
-------------------------------------------