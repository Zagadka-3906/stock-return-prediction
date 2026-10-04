# 第15轮：扩展MLP结构与训练轮数分用途集成

本轮完成88种不同输出配置、107条评分记录。R14基准 **0.449332307407**，最高连续验证分 **0.449605455335**，提升 **0.000273147929**。

| 阶段 | 评分记录 | 截至阶段结束的最高分 | 相比前阶段变化 |
| --- | ---: | ---: | ---: |
| 三个用途独立集成 | 61 | 0.449564265 | +0.000231957 |
| 用途最优设置组合 | 8 | 0.449564265 | +0.000000000 |
| 集成权重细搜 | 18 | 0.449602862 | +0.000038598 |
| 输出细调 | 20 | 0.449605455 | +0.000002593 |

具体方法的起点和自适应细搜规则已在评分前冻结。累计最高分是选模过程记录，阶段差异不表示独立因果贡献；重复基准不计作新的模型训练。



首次校准遇到冷缓存日期前缀尺寸错误；通过单独的缓存切片适配器恢复，原始冻结源文件、模型参数、评分记录与选中预测数组均保留。完整输出逐位一致、冷缓存日期前缀、校准CSV官方评分和候选复放重新通过；适配器证据见本轮 `calibration_cache_recovery.json`。

| 指标 | R14基准 | 本轮选中方案 | 变化 |
| --- | ---: | ---: | ---: |
| Rank IC | 0.120182525 | 0.120785574 | +0.000603049 |
| 年化超额收益 | 36.959685% | 36.970327% | +0.010643个百分点 |
| 平均换手率 | 3.206585% | 3.206585% | +0.000000个百分点 |

所选配置：

```json
{
  "top_ensemble_name": "lgb1_xgb1_two0_gru1",
  "ensemble_name": "lgb1_xgb1_two1_gru2.25",
  "top_slow_weight": 0.26,
  "slow16_weight": 0.27,
  "priority_signal": "top",
  "add_priority_weight": 0.0,
  "drop_priority_weight": 0.0,
  "membership_signal": "independent",
  "membership_mode": "global",
  "membership_w5a_weight": 0.75,
  "retention": 0.984,
  "limit_up_delta": 0.075,
  "membership_ensemble_name": "lgb0.75_xgb1_two1_gru2.25",
  "membership_slow_weight": 0.24,
  "recipe": {
    "type": "raw_rank_mix",
    "components": [
      {
        "type": "model",
        "seed": 2026,
        "fraction": 0.175,
        "rounds": 90,
        "params": {},
        "samples": 8,
        "postprocessing": {
          "alpha": 0.9,
          "bonus": 0.3,
          "mode": "top_only",
          "weight": 0.25,
          "restore_lower": true,
          "top_current_weight": 1.0
        },
        "weight": 0.25
      },
      {
        "type": "model",
        "seed": 2026,
        "fraction": 0.175,
        "rounds": 180,
        "params": {},
        "samples": 8,
        "postprocessing": {
          "alpha": 0.9,
          "bonus": 0.3,
          "mode": "top_only",
          "weight": 0.25,
          "restore_lower": true,
          "top_current_weight": 1.0
        },
        "weight": 0.75
      }
    ],
    "postprocessing": {
      "alpha": 0.9,
      "bonus": 0.3,
      "mode": "top_only",
      "weight": 0.25,
      "restore_lower": true,
      "top_current_weight": 1.0
    }
  },
  "membership_power": 1.0,
  "membership_memory": 0.025,
  "diverse_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "rank512_e32",
      "weight": 0.1
    },
    "rest": {
      "model": "rank512_e32",
      "weight": 0.2
    }
  }
}
```

采用2020—2024逐年向前验证，连接1,212日、5,635,800行，年度边界换手连续计算。基准逐元素复现、成熟过去标签收益映射、实际验证CSV官方评分、所选方法标签置空和日期前缀检查、模型重载、预测重放、CSV键值及秩检查均通过。基础模型重新训练：True。

本轮未读取测试标签、未打新测试分；各验证年份此前均已查看，反复选模偏差未校正。候选单独保存于 `candidates/optimization_20261003_r15/submission.csv`，正式交付指针和历史候选保留。逐条评分见同目录的 `optimization_ranking_20261003_r15.json`。
