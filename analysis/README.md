# 后续研究与验证工具

本目录承载后续模型搜索、年度训练、官方评分、方案冻结、因果检查、候选推理、榜单登记、GitHub同步和Windows运行管理。大量脚本按轮次和版本保留，包含失败恢复过程；文件数量不是独立模型数量。

2026-10-11已确认历史重建测试收益影响过推荐及研究路线；现有方案不能宣称严格训练内选模，见[合规更正](../docs/SELECTION_COMPLIANCE.md)和[机器可读状态](../selection_compliance.json)。旧核验通过与榜单登记是当时事实，不消除历史选择反馈。

新读者先看[项目首页](../README.md)、[模型与验证](../docs/METHODS.md)和[目录与记录](../docs/REPOSITORY_GUIDE.md)。实际运行条件见[使用与复现](../docs/GETTING_STARTED.md)。

## 当前阅读入口

| 本机文件 | 含义 |
|---|---|
| `alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json` | 最新37模型高分候选及提交CSV，正式完整榜待登记 |
| `actual_fraction101_delivery_bundle137_verification_v1_20261011.json` | 已核验方案ZIP与弃用模型清理汇总 |
| `latest_verified_submission_delivery_v2_20261008.json` | 第189轮正式已登记交付 |
| `complete191_plus_completed_raw_TRAIN_score_catalog_location_v7_20261011.json` | 18,959项训练评分明细的位置及核验 |
| `optimization_20261003_r191/full_registration_execution.json` | 第191轮正式登记的实际完成终态 |
| `service_owned_workflows_20261006/` | 每个独立工作流的定义、进程身份、日志与实际终态 |

Git克隆未必包含每个本机运行文件；外部读者请通过[成果与交付](../docs/RESULTS.md)访问已发布的 `validation_sync/`归档。

## 执行与证据

`prepare_`、`run_`、`seal_`、`publish_`及 `register_`分别处理准备、运行、封存、发布与正式登记，按对应协议依赖执行。某阶段 `passed`不代表下游全部完成。选模、冻结与提交流程以[后续选模标准](../后续选模标准.md)为准。

历史脚本可能依赖本机D/E盘路径、旧版本源码哈希、父方案、完整数据和已清理权重。不要批量执行目录中的脚本或覆盖旧输出。新的尝试应在新协议与独立目录中保存；已经冻结的候选、服务失败终态和评分记录继续保留原始内容。

模型优化已按用户截止安排暂停。阅读、改写说明或整理已有成果不表示授权自动恢复训练、评分队列或停工守护。
