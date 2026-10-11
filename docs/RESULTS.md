# 成果与交付

状态日期：2026-10-11。这里的“官方评分”指使用赛题官方脚本计算训练内部验证区间的指标；比赛平台测试成绩另行判定。

**选模来源合规暂停：历史上从测试X重建的343天收益影响了推荐与研究路线，当前方案继承该研究链。撤回严格训练内选模的推荐结论。** 下表的分数、推理通过和榜单登记仍按原事实保留，不作为选模来源合规证明；详见[合规更正](SELECTION_COMPLIANCE.md)。

## 当前方案

| 方案 | 训练内部连接S | 当前状态 |
|---|---:|---|
| 60/120日一致性融合，15%保护区，候选101 | **0.4514612196682616** | 37模型重载、独立全量复算、CSV重放、80日冷启动、源码封存、ZIP核验和main发布完成；正式完整榜待登记 |
| 60/120日一致性融合，20%保护区，候选85 | 0.4514555940046018 | 完整核验的保留备份 |
| 第189轮已登记交付 | 0.4514130257498636 | 正式完整资格登记已完成的交付指针，继续保留 |

最新候选与已登记交付不是同一状态。“候选101”是后续辅助流程编号，不代表正式第101轮。第191轮正式登记已完成；第192轮已有48项评分，但登记中断，没有完整完成回执，不计入已完成正式轮次。

最新37模型候选的八项指标：

| 指标 | 数值 |
|---|---:|
| IC均值 | 0.12280208457197295 |
| IC标准差 | 0.11111633330974156 |
| ICIR | 1.1051668185419405 |
| 正IC天数占比 | 0.8960396039603961 |
| Top组年化超额 | 0.3735093425702569 |
| Top组年化绝对收益 | 0.39900309663051436 |
| 平均换手率 | 0.032374723105348766 |
| 综合S | 0.4514612196682616 |

仅IC均值、Top年化超额和平均换手进入综合分。分数范围与各指标小数值不能当作百分制成绩。

## 提交文件和方案包

提交CSV包含 **1,599,600行、344个交易日、4,650只股票**，列名及顺序为 `ts_code, trade_date, pred`。最新方案未向比赛平台上传，未使用实际测试标签进行新增评分。

维护者本机交付目录：

```text
E:\赛题五_最终提交\已核验候选_60与120日保护比例8项101_20261011\
  submission.csv
  submission_manifest.json
  方案使用说明.md
  方案包核验.json
  赛题五_高分方案_S0.45146122_20261011.zip
```

这些E盘路径不在其他读者的电脑上。ZIP在本地保存，没有发布为GitHub Release附件；它包括完整候选、37个权重、冻结源码、配置与证据，共16,600个条目，压缩文件160,925,612字节，约153.47 MiB。每个条目已核对SHA256。

```text
submission.csv SHA256:
18c4c67c7b457eabb3e8c89048df2ae67bc64197b77d0d9e8225ef8a9399f438

ZIP SHA256:
d3928b57be66ee0747eb0751c22923ff804e2496b32568beb9643594c80ee6d5
```

取得文件后可在PowerShell使用 `Get-FileHash -Algorithm SHA256 -LiteralPath '文件路径'`核对。详细配置和模型校验见[已发布候选归档](../validation_sync/Actual_consensusFraction101_complete_candidate_sources_and_submission_v1_20261011/)。大提交CSV在该归档中以gzip压缩文本保存。

## 完整榜和评分明细在哪

正式完成记录覆盖至第191轮，正式评分实例17,753项；新增已完成原始TRAIN评分实例1,206项，共 **18,959项评分记录**。包含复用、对照、参数变化和重复记录，不能宣称尝试了18,959个独立模型。

最新版v7的评分CSV与已核验v5逐字节相同，仅更新完整候选交付状态。它补充评分明细，不取代正式完整榜登记；也没有把第192轮登记补写为完成。

- [全部训练验证分数明细（CSV.gz）](../validation_sync/Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011/external_metadata/d4e902ebc06db7788115eb9374ede012f66b203d3cc60ec44bac55cdc9e7e938_全部训练验证分数明细.csv.gz)
- [排除已知非因果限制后的明细（CSV.gz）](../validation_sync/Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011/external_metadata/a77376323e14d93bb9ab523fbb5931cd6169d2d10aa0f6ce9df0b9006cad4fdd_排除已知非因果限制后的训练分数明细.csv.gz)
- [榜单位置与核验指针](../validation_sync/Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011/analysis/complete191_plus_completed_raw_TRAIN_score_catalog_location_v7_20261011.json)

解压gzip后按CSV阅读，保留 `known_restriction`、`qualification`、`source`、`source_sha256`和 `official_capsule_sha256`等列。原“排除已知非因果限制”的CSV仅按当时记录的数值限制过滤，未排除本次确认的历史测试反馈；不能将它直接当作合规选模榜。另见[当前选模状态](../selection_compliance.json)。

## 核验与发布证据

- [最新候选交付指针](../validation_sync/Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011/analysis/alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json)
- [ZIP与清理核验记录](../validation_sync/Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011/analysis/actual_fraction101_delivery_bundle137_verification_v1_20261011.json)
- [最新源码包、榜单与清理归档](../validation_sync/Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011/)
- [机器可读成果摘要](latest_results.json)

候选源码与CSV归档提交为 `59c2553fcd61371f8f55f26b16aa333d8729071f`；方案包核验、榜单与清理记录提交为 `363b04accad09d792a53de06f0a3cde3dba11146`。这些是成果快照的提交号，文档后续更新会使main继续前进。

## 结论的边界

最新候选的训练验证S略高于上一完整候选，提升主要来自IC，年化超额与换手保持相同。长期反复搜索同一验证区间会产生选择偏差，目前未校正；不能据此承诺盲测或交易表现。

本次未修改官方评分器、未使用缓存的两次全量复核均得到S=0.4514612196682616，当前数值评分没有因此被撤销。但历史测试结果曾反馈到选模路线，新阶段未再读取测试标签不能修复这一事实；最新研究候选及第189轮已登记方案均不自动取得严格训练内选模推荐。模型优化继续暂停。
