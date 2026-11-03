# 后续研究与核验脚本

本目录保存后续模型研究、训练期评分、冻结、推理、候选封装、完整榜登记和Windows运行管理源码。脚本往往对应具体轮次与执行版本，适合沿某个结果的依赖链阅读。

## 从具体路线进入

| 目标 | 源码或指针 | 阅读前提 |
|---|---|---|
| 理解直接收益基线 | `train_only_baseline143_v1_20261011.py` | [设计与时间边界](../docs/TRAIN_ONLY_BASELINE143.md) |
| 阅读修正后的基线推理 | `train_only_baseline143_inference_v3_20261011.py` | 需要其导入的原训练脚本与完整工作目录 |
| 查37模型候选 | `alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json` | 公开副本从[结果页](../docs/RESULTS.md)进入 |
| 查包内条目核验 | `actual_fraction101_delivery_bundle137_verification_v1_20261011.json` | 对应候选和原ZIP |
| 查评分目录 | `complete191_plus_completed_raw_TRAIN_score_catalog_location_v7_20261011.json` | 18,959是评分记录，不是模型数量 |
| 查正式登记 | `optimization_20261003_r191/full_registration_execution.json` | 以实际终态为准 |

本机生成的部分JSON和运行目录不在原路径分发，相同证据保存在`validation_sync/`快照中。源码克隆也不包含所有模型、数据和缓存。

## 读懂脚本阶段

`prepare_`通常准备输入，`run_`执行研究，`seal_`封存，`register_`登记，`publish_`发布。前缀是定位线索，实际依赖和行为仍需查看代码与协议；某阶段成功不代表整条链完成。

带版本号的脚本可能用于修复连接列顺序、路径、服务恢复或核验逻辑，不一定增加新模型。不要按文件名批量运行，也不要用较新文件覆盖冻结快照。

## 开展自己的实验

2026-11-03已移除653个没有被保留代码、当前文档和状态记录引用的旧发布、监控等运维脚本；每个文件都有字节相同的冻结副本。需要查找旧路径时使用`tools/find_archive_record.py`，见[归档维护](../docs/REPOSITORY_CLEANUP.md)。模型研究、训练、推理与必要依赖继续保留。

先读[系统架构](../docs/ARCHITECTURE.md)与[实验比较约定](../后续选模标准.md)，使用独立目录记录数据、协议和输出。根目录固定基准通常比重放历史服务更适合作为起点。

旧集成路线的测试期反馈、重复搜索和结果解释见[研究边界](../docs/SELECTION_COMPLIANCE.md)。本次文档更新不启动或恢复历史训练与优化服务。
