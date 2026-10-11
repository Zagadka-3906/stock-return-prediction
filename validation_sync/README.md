# 验证归档导航

此目录保存已完成研究的源码、协议、评分、哈希与执行证据。为避免每轮重复检出全套历史源码和累计排名展示，2026-10-11已整理当前main中的归档文件。

## 当前主要入口

| 入口 | 内容 |
|---|---|
| [最新完整候选](Actual_consensusFraction101_complete_candidate_sources_and_submission_v1_20261011/) | S=0.4514612196682616，37模型推理、冻结源码及提交CSV归档 |
| [方案包、评分明细与清理记录](Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011/) | 18,959项训练评分明细、ZIP哈希、交付指针和弃用模型清理记录 |
| [第191轮正式完整归档](round191/) | 17,753项正式评分实例的完整累计榜、六视图及实际浏览器QA |
| [第189轮归档](round189/) | 保留的正式已登记交付所对应轮次 |
| [项目文档更新](Actual_project_documentation138_refresh_20261011/) | README、About与文档重写的核验记录 |
| [归档路径查询清单](archive_index_20261011.jsonl.gz) | 本次移除路径、相同内容保留路径、Git blob及历史提交 |
| [历史测试反馈与选模合规更正](Actual_selection_compliance142_correction_v1_20261011/) | 343天测试收益重建、推荐及研究反馈证据、两次直接官方评分复核和当前推荐暂停 |

## 整理规则

当前方案、第189/191轮正式归档、最新评分明细和唯一记录继续保留。同一Git blob的历史导出副本只删冗余路径，清单给出仍保留的相同内容文件。较早轮次的累计排名HTML及重构JSON gzip/分片是可生成的展示副本，保留最新第191轮完整累计榜，原始评分与控制记录不因删除展示副本而删除。

历史归档中的 `manifest.json`、源码绑定和发布回执是当时快照，所列路径应在对应历史提交读取；它们不保证所有重复展示路径仍在当前main检出。原文件继续保存在Git历史中，本次不重写历史或清除Git对象。

旧评分与推理 `passed`记录不证明整个选模历史符合训练内部标准。2026-10-11确认历史重建测试收益影响过研究路线，当前状态以[选模合规更正](../docs/SELECTION_COMPLIANCE.md)和[状态JSON](../selection_compliance.json)为准；原“排除已知非因果限制”评分表没有过滤这一历史反馈。

查询示例，在项目根目录运行：

```powershell
python tools/find_archive_record.py '原归档相对路径'
```

返回的 `retained_path`（如有）是当前相同内容副本；`historical_url`指向整理前提交中的原文件。详情见[仓库整理说明](../docs/REPOSITORY_CLEANUP.md)。
