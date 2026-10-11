# 目录与记录

## 目录地图

| 路径 | 用途 | 阅读或运行时要注意 |
|---|---|---|
| `README.md`、`ABOUT.md`、`docs/` | 项目介绍、方法、使用入口和最新状态 | 新读者从这里开始 |
| `src/` | 特征、评分辅助、集成、后处理等通用逻辑 | 63项基础特征与67项历史基准逻辑在这里 |
| `config/` | 固定基准的特征顺序与16种子集成配置 | 不代表最新37模型候选的全部配置 |
| `run.py` | 早期LightGBM基准与特征构建入口 | `all`不是最新高分方案的一键复现 |
| `train_ensemble.py`、`predict.py` | 历史67特征XGBoost基准 | 参数支持见各脚本 `--help` |
| `evaluate.py`、`evaluate.R` | 赛题评分代码 | Python入口会读取指定目录中的X/Y评分文件 |
| `experiments/` | 早期主题研究、诊断和审计源码 | 多数依赖历史产物，见[实验索引](../experiments/README.md) |
| `analysis/` | 后续选模、控制、冻结、验证、推理和登记工具 | 不是一组可以任意顺序运行的脚本；运行有冻结与依赖关系 |
| `results/` | 每轮成果摘要与历史结果 | 轮次、研究波次、配置数、评分记录数和模型数不能混用 |
| `validation_sync/` | 已提交main的验证及交付归档 | 包括源码副本、协议、指标、哈希、控制与发布记录；部分大文本为 `.gz` |
| `data/` | 本地原始行情、特征缓存和特征清单 | 原始比赛数据不随普通Git克隆提供 |
| `models/`、`candidates/` | 本地基准权重和候选方案 | 大量权重或候选二进制产物由D/E盘保存，部分已清理 |
| `deliveries/`、`outputs/`、`validation/` | 早期交付、入口输出与验证产物 | 按版本理解，不能只按文件修改时间选“最新” |
| `tmp/` | 运行临时文件、矩阵和工作流缓存 | 可能映射到E盘；不是成果索引 |

`validation_sync/`是Git发布工作副本中的主要归档目录，本机研究目录可能没有检出所有归档文件。GitHub以 `main`为唯一工作分支。

2026-10-11已整理重复导出与旧累计排名展示。保留文件、历史路径查询及存储影响见[仓库整理说明](REPOSITORY_CLEANUP.md)与[验证归档导航](../validation_sync/README.md)。旧发布manifest按对应历史提交读取。

## 一份验证记录包含什么

常见文件的职责：

- `protocol.json`：数据、窗口、方法、预定检查与输入哈希。
- `selection.json`：选择结果、分数及预测前冻结信息。
- `calibrated_csv_official.json`：最终收益映射CSV的官方指标。
- `verification.json`：实际执行的模型重载、独立推理、CSV与因果对照结果。
- `manifest.json`：封存文件的SHA256和大小。
- `full_registration_execution.json`：正式完整榜登记是否实际完成。
- `service_execution.json`：独立工作流的实际终态；`passed`与`failed`保留原义。
- 发布回执：提交SHA、main分支、远端核验及原始Git blob检查。

“冻结”“已评分”“完整推理通过”“正式榜已登记”“已封装”和“比赛平台已提交”是不同状态。判断资格需看相应记录，不能由某个上游 `passed`推断全部完成。

## 当前状态指针

| 本机文件 | 指向的状态 |
|---|---|
| `analysis/alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json` | 最新高分候选，S=0.4514612196682616，完整推理和封装已通过，正式完整榜待登记 |
| `analysis/actual_fraction101_delivery_bundle137_verification_v1_20261011.json` | 方案ZIP条目核验与清理汇总 |
| `analysis/latest_verified_submission_delivery_v2_20261008.json` | 正式资格登记已完成的第189轮交付，S=0.4514130257498636 |
| `analysis/complete191_plus_completed_raw_TRAIN_score_catalog_location_v7_20261011.json` | 18,959项训练评分明细与最新已核验交付位置 |
| `active_release.json` | 早期交付指针，保留历史用途；不作为最新高分候选入口 |

外部读者可从[最新状态](latest_results.json)和[成果与交付](RESULTS.md)进入已发布归档，不需要猜测本机路径。

## 历史记录与已清理模型

本项目按用户要求清理未采用的模型权重、恢复缓存和部分历史副本，保留分数、配置、SHA256及审计记录。2026-10-11本次清理删除267个弃用权重及缓存，逻辑文件大小合计22,194,089,456字节。最新候选及保留交付所需模型已经在清理后重新核对哈希。

历史记录中的模型路径和旧的“权重保留”状态反映当时快照；后续清理清单解释哪些文件已删除。文件不存在不等于历史评分被取消，但已删除权重的方案不能承诺无需重训即可复现。

## 为何有很多带版本号的脚本

后续研究既保存科学结果，也保存Windows进程管理、磁盘迁移、缓存复用与失败恢复证据。新版本通常用于修复独立运行阶段或保留原失败记录，不表示一定训练了一个新模型。

维护时保持冻结候选和原始服务终态不变。文档更新与运行控制分开；阅读或更新说明不应恢复已暂停的训练、评分守护或自动优化队列。
