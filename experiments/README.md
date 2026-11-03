# 早期实验源码索引

本目录按主题保存早期量价建模与模型组合研究。阅读时先选择研究问题，再看对应源码的输入、配置和输出路径。原运行产物分布于本地历史目录及`validation_sync/`归档，部分权重与缓存已清理。

## 按问题找源码

| 研究问题 | 代表源码 |
|---|---|
| 回归、排名与参数如何影响结果 | `ranking_candidates.py`、`optuna_regression.py`、`next_steps_candidates.py` |
| 平滑与名单保护如何改变换手 | `cached_recheck.py`、`protected_top.py`、`top_internal.py` |
| 收益辅助信号是否与排名互补 | `return_head_models.py`、`return_pooled_models.py`、`return_market_models.py` |
| 多种子与检查点如何组合 | `seed_ensemble.py`、`wave14_seed_average.py`、`wave16_seed_curve.py` |
| 特征扩展与同伴信息是否有帮助 | `feature_expansion.py`、`wave9_exploratory.py`、`wave21_peer_lags.py` |
| 新信号能否在不同配方上复现 | `wave19_three_axes.py`、`wave22_additivity.py`、`wave23_validation.py` |
| 神经网络能否提供不同信号 | `sequence_model.py`、`sequence_training.py`、`r6_transformer.py` |
| 标签、时点、执行与成本如何影响解释 | `execution_timing.py`、`backtest_causal_portfolio.py`、`cost_execution.py` |
| 评分与缓存是否一致 | `revalidate_fold_local.py`、`official_seed_development.py`、`audit_*.py` |
| 如何组织多种子精确重算 | `wave24_recompute_validation.py` |

`final_sweep_*.py`和部分`r*_*.py`研究历史候选、分层排序与多模型组合。`finalize_r6.py`、`finalize_r7.py`和`finalize_r9.py`偏向证据封装与核验；文件名中的`final`不表示今天仍是推荐入口。

## 与通用代码的关系

已抽取的通用逻辑位于`src/research_stats.py`、`src/postprocessing.py`、`src/peer_features.py`和`src/pooled_target.py`。根目录训练与预测命令运行固定67特征XGBoost配方；后续复杂研究主要位于`analysis/`。

历史源码可能检查原文件哈希、依赖特定父方案或使用本机绝对路径。重放原协议应使用对应冻结快照；扩展方法则在新目录建立协议与产物，避免覆盖原记录。

[安装与运行](../docs/GETTING_STARTED.md) · [方法详解](../docs/METHODS.md) · [结果索引](../results/README.md) · [研究边界](../docs/SELECTION_COMPLIANCE.md)
