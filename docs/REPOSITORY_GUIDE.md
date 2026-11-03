# 仓库导航

读源码可以从根目录入口、`src/`和`config/`开始；核查特定研究结论则从`results/`索引进入`validation_sync/`的冻结记录。项目包含大量历史快照，文件数量与模型数量没有一一对应关系。

## 目录职责

| 路径 | 内容 | 建议读法 |
|---|---|---|
| `README.md`、`ABOUT.md` | 项目定位、能力与阅读入口 | 首次了解项目 |
| `docs/` | 数据、方法、架构、运行与复现 | 按[文档导航](README.md)选择 |
| `src/` | 特征、集成、后处理和评分辅助 | 理解通用计算逻辑 |
| `config/` | 63项基础列顺序、固定67特征集成配方 | 与`src/ensemble.py`对照 |
| `run.py` | 特征构建与早期LightGBM流程 | `features`可供固定基准共用 |
| `train_ensemble.py`、`predict.py` | 固定XGBoost集成训练与重载推理 | 从CLI参数追到`src/ensemble.py` |
| `evaluate.py`、`evaluate.R` | 原始评分脚本 | 确认指标与过滤口径 |
| `experiments/` | 早期主题研究和诊断源码 | 先读[实验索引](../experiments/README.md) |
| `analysis/` | 后续模型、冻结、推理、登记与运行工具 | 先读[研究脚本说明](../analysis/README.md) |
| `tests/` | 预测与评分相关核查脚本 | 按脚本所需数据运行 |
| `results/` | 指标JSON、历史轮次摘要与结果指针 | 结合来源和状态字段阅读 |
| `validation_sync/` | 冻结源码、协议、哈希、执行和发布记录 | 按特定候选查证 |
| `tools/` | 归档检索及文档维护工具 | 见各工具参数 |

## 主要在本地生成的内容

| 路径 | 内容 |
|---|---|
| `data/` | 原始行情、特征Parquet与特征清单 |
| `models/` | 基准原生模型 |
| `candidates/` | 研究候选与组合依赖 |
| `outputs/`、`validation/` | 预测、验证输入和运行结果 |
| `deliveries/`、`releases/` | 历史交付目录 |
| `tmp/` | 临时矩阵与工作流缓存 |

这些目录中的数据和大模型产物通常不随Git克隆分发。历史机器有D/E盘迁移和清理记录，因此旧路径可能只存在于manifest中。缺少文件时，先查[归档维护](REPOSITORY_CLEANUP.md)，不要据修改时间随意拼接不同候选。

## 常见文件如何配合

| 文件 | 记录内容 |
|---|---|
| `protocol.json` | 数据、窗口、方法、预设检查与输入哈希 |
| `selection.json` | 候选选择、分数与预测前冻结信息 |
| `calibrated_csv_official.json` | 最终映射后CSV的评分 |
| `verification.json` | 模型重载、独立推理、CSV或前缀核验 |
| `manifest.json` | 文件清单、大小与SHA256 |
| `full_registration_execution.json` | 正式完整榜登记的实际终态 |
| `service_execution.json` | 某次运行服务的实际结果 |
| 发布回执 | Git提交、分支与远端内容核验 |

“已评分”“推理通过”“已封装”“已登记”描述不同阶段。旧记录的`passed`应按对应阶段解释，不应概括成所有研究问题都已经解决。

## 主要历史指针

| 文件或归档 | 所描述的快照 |
|---|---|
| `docs/latest_results.json` | 面向读者的历史指标摘要，含两条主要路线 |
| `results/train_only_baseline143_v1_20261011.json` | 单模型直接收益基线的执行与结果 |
| `analysis/alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json` | 37模型候选，已封装，完整榜待登记 |
| `analysis/latest_verified_submission_delivery_v2_20261008.json` | 第189轮已登记交付，属于旧集成研究链 |
| `analysis/complete191_plus_completed_raw_TRAIN_score_catalog_location_v7_20261011.json` | 18,959项训练评分目录 |
| `active_release.json`、`selection_compliance.json` | 原发布与历史研究来源更正状态 |

部分`analysis/`本机生成JSON没有在该原路径检出，公开副本位于相应`validation_sync/`归档。[结果与产物](RESULTS.md)提供了可直接访问的入口。

## 版本、轮次与数量

脚本名中的版本通常用于保存执行修复、路径迁移或失败恢复，不意味着增加了一个新模型。正式轮次、研究波次、候选编号、评分记录数与原生模型数也不能相互替代。

冻结记录按原版本保存。对外说明可以更新，已绑定哈希的历史证据应继续按对应提交解释。[研究边界](SELECTION_COMPLIANCE.md)集中说明后续更正对旧记录的影响。
