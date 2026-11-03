# 验证与冻结归档导航

本目录保存研究源码快照、协议、指标、文件哈希及实际执行证据。查证结论时，应先定位候选与快照，再读取对应文件；整个目录不是一个可按顺序运行的应用程序。

## 主要入口

| 归档 | 内容 |
|---|---|
| [直接收益基线143](TRAIN_only_baseline143_v1_20261011/) | 固定LightGBM基线的源码与执行记录 |
| [37模型候选](Actual_consensusFraction101_complete_candidate_sources_and_submission_v1_20261011/) | 冻结源码、推理证据与压缩提交CSV |
| [完整包与评分目录](Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011/) | ZIP核验、18,959项评分目录与清理记录 |
| [第191轮](round191/) | 已完成正式登记的累计榜与核验 |
| [第189轮](round189/) | 历史已登记交付的轮次快照 |
| [测试反馈更正](Actual_selection_compliance142_correction_v1_20261011/) | 重建收益、反馈链条与评分复核证据 |
| [原文档更新快照](Actual_project_documentation138_refresh_20261011/) | 2026-10-11的旧文档与当时记录 |
| [归档路径目录](archive_index_20261011.jsonl.gz) | 旧路径、相同内容副本与历史提交映射 |

## 按快照解释文件

`manifest.json`绑定的是生成时的文件与哈希。某份旧导出在当前main被去重后，原路径应从对应提交读取，或查找相同Git blob的保留路径。完整归档查询方法见[归档维护](../docs/REPOSITORY_CLEANUP.md)。

```powershell
python tools/find_archive_record.py '原归档相对路径'
```

历史材料可能包含原机器绝对路径、旧运行说明与过时推荐。它们保留作为证据，不应复制成今天的使用指引。当前解释以[文档导航](../docs/README.md)、[结果页](../docs/RESULTS.md)和[研究边界](../docs/SELECTION_COMPLIANCE.md)为入口。

## 压缩与重组

大文本可能以`.gz`保存，部分旧展示曾使用分片。按原manifest顺序恢复后，再核对SHA256。不要仅凭文件名相似就将不同轮次分片混合。

本目录中的`passed`描述特定检查或执行阶段，并不自动证明研究选择独立、方案可跨机器直接运行或已经发布全部二进制权重。
