# 第 66 轮验证

连续向前验证官方分：**0.451008106892**；本轮增量：+0.000000000000。

本轮完整评分记录 218 条；累计连接榜 9822 条。

选择冻结、官方评分复核、因果前缀检查、候选推理及文件哈希核验均通过。验证年份已多次参与选择，累计选择偏差尚未校正；本轮没有候选测试评分。

- `selected_scheme.json`：冻结赢家及完整参数权威图。
- `all_round_configurations.json.gz`：所有本轮完整配置，可用 Python gzip 解压。
- `ranking_round.csv`、`ranking_all.csv`：本轮与累计完整榜。
- `protocol.json`、各检查 JSON 及 `manifest.json`：验证证据与原始文件 SHA256。

方案代码位于仓库的 `analysis/`、`experiments/` 和 `src/`。完整复现需要本地数据、历史缓存及模型文件；文件来源和 SHA256 保存在冻结协议与候选清单中。

第66轮原始来源解析因候选文件尚未生成而失败；原协议和失败证明保持原样。实际恢复的完整执行证明为 `provenance_scope_execution_recovery_v3_20261005.json`，恢复冻结来源为 `recovery_frozen_execution_v3_20261005.json`。只有实际恢复的全部科学检查和最终全量哈希复核通过后，才导出本目录。
