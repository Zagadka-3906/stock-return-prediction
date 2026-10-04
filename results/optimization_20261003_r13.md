# 第13轮：非线性持仓融合与逐股因果平滑

本轮完成37种不同输出配置、52条评分记录。R12基准 **0.449137312660**，最高连续验证分 **0.449332307407**，提升 **0.000194994746**。

| 阶段 | 评分记录 | 截至阶段结束的最高分 | 相比前阶段变化 |
| --- | ---: | ---: | ---: |
| 非线性融合 | 12 | 0.449137313 | +0.000000000 |
| 逐股平滑 | 10 | 0.449137313 | +0.000000000 |
| 组合与细搜 | 15 | 0.449160590 | +0.000023277 |
| 输出细调 | 15 | 0.449332307 | +0.000171717 |

具体方法的起点和自适应细搜规则已在评分前冻结。累计最高分是选模过程记录，阶段差异不表示独立因果贡献；重复基准不计作新的模型训练。

| 指标 | R12基准 | 本轮选中方案 | 变化 |
| --- | ---: | ---: | ---: |
| Rank IC | 0.120124522 | 0.120182525 | +0.000058003 |
| 年化超额收益 | 36.899798% | 36.959685% | +0.059886个百分点 |
| 平均换手率 | 3.203964% | 3.206585% | +0.002622个百分点 |

所选配置：

```json
{
  "top_ensemble_name": "lgb1_xgb1_two0_gru1",
  "ensemble_name": "lgb1_xgb1_two1_gru2.25",
  "top_slow_weight": 0.26,
  "slow16_weight": 0.23,
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
  "membership_memory": 0.025
}
```

采用2020—2024逐年向前验证，连接1,212日、5,635,800行，年度边界换手连续计算。基准逐元素复现、成熟过去标签收益映射、实际验证CSV官方评分、所选方法标签置空和日期前缀检查、模型重载、预测重放、CSV键值及秩检查均通过。基础模型重新训练：False。

本轮未读取测试标签、未打新测试分；各验证年份此前均已查看，反复选模偏差未校正。候选单独保存于 `candidates/optimization_20261003_r13/submission.csv`，正式交付指针和历史候选保留。逐条评分见同目录的 `optimization_ranking_20261003_r13.json`。
