# 历史实验源码索引

本目录保留模型研究与验证源码。每一轮实验曾在独立子目录中保存冻结协议、预测缓存、评分和审计结果；本次整理将这些运行产物移至项目目录外的本地历史归档，避免研究源码与大量中间文件混在一起。

当前可直接使用的主流程是根目录的 `run.py`、`train_ensemble.py` 和 `predict.py`。本目录记录研究路径，其中许多程序依赖先前轮次的结果，不宜按文件名逐个执行。

## 研究主题

| 主题 | 代表性源码 | 主要问题 |
|---|---|---|
| 回归与排序基准 | `ranking_candidates.py`、`optuna_regression.py`、`next_steps_candidates.py` | 不同目标和参数怎样影响综合评分？ |
| 名单稳定性与后处理 | `cached_recheck.py`、`protected_top.py`、`top_internal.py` | 平滑、持续性奖励和头部内部排序如何影响换手及收益？ |
| 收益辅助模型 | `return_head_models.py`、`return_pooled_models.py`、`return_market_models.py` | 收益标签归一化与辅助融合是否提供额外信息？ |
| 随机种子集成 | `seed_ensemble.py`、`wave14_seed_average.py`、`wave16_seed_curve.py` | 种子数量、秩平均和集成多样性带来多少变化？ |
| 特征扩展 | `feature_expansion.py`、`wave9_exploratory.py`、`wave21_peer_lags.py` | 扩展特征、同伴分组与滞后信息是否改善表现？ |
| 配对与交互验证 | `wave19_three_axes.py`、`wave22_additivity.py`、`wave23_validation.py` | 特征、训练配方与种子效应能否区分？ |
| 神经网络 | `sequence_model.py`、`sequence_training.py`、`r6_transformer.py` | MLP、GRU、Transformer 能否补充树模型？ |
| 时间与交易可行性 | `execution_timing.py`、`backtest_causal_portfolio.py`、`cost_execution.py` | 标签成熟时点、成交约束和成本如何改变解释？ |
| 评分与审计 | `revalidate_fold_local.py`、`official_seed_development.py`、`audit_*.py` | 官方口径、特征时点和产物一致性是否成立？ |
| 年度分数重算 | `wave24_recompute_validation.py` | 保存预测能否复现八种子及十六种子的年度分数？ |

`final_sweep_*.py` 与各轮 `r*_*.py` 保留历史候选搜索、残差 / 互补信号和独立诊断。`finalize_r6.py`、`finalize_r7.py`、`finalize_r9.py` 是研究证据封存和核验工具，依赖归档的冻结材料。

## 使用历史源码的注意事项

1. 先阅读脚本顶部说明、输入路径与命令行参数，确认依赖哪一轮协议和缓存。
2. 旧脚本中的 `releases/`、`deliveries/` 及带日期的实验目录指向历史归档中的材料；本仓库不携带这些产物。
3. 部分实验会校验历史源文件哈希。整理后源码和路径已经变化，复核原协议时应在原始归档副本中执行；开展新实验时应创建新的协议和运行目录。
4. 不覆盖旧协议、结果或保存模型。历史收益标签用于回顾诊断；当前训练和预测入口不把它们作为模型输入。

核心数值逻辑已提取到 `src/research_stats.py`、`src/postprocessing.py`、`src/peer_features.py`、`src/pooled_target.py`，当前方案的配置在 `config/`。可浏览的成果摘要集中于 [results/](../results/)，项目整体说明见 [README](../README.md)。
