# 第29轮：未来一日线性信号的完整输出增量集成

本轮完成87种不同输出配置、104条评分记录。R28基准 **0.450746179510**，最高连续验证分 **0.450757224070**，提升 **0.000011044560**。

| 阶段 | 评分记录 | 截至阶段结束的最高分 | 相比前阶段变化 |
| --- | ---: | ---: | ---: |
| 6种线性信号独立用途比较 | 73 | 0.450755437 | +0.000009258 |
| 用途最优设置组合 | 8 | 0.450755437 | +0.000000000 |
| 权重细搜 | 18 | 0.450755437 | +0.000000000 |
| 涨停股输出偏移细调 | 5 | 0.450757224 | +0.000001787 |

具体方法的起点和自适应细搜规则已在评分前冻结。累计最高分是选模过程记录，阶段差异不表示独立因果贡献；重复基准不计作新的模型训练。

本轮评分记录中，87次重新调用官方评分，17次复用完全相同CSV及验证输入的已有官方结果。CSV、验证数据、评分代码和运行库版本共同确定缓存；对应证据已随选定方案冻结。



| 指标 | R28基准 | 本轮选中方案 | 变化 |
| --- | ---: | ---: | ---: |
| Rank IC | 0.121482836 | 0.121510447 | +0.000027611 |
| 年化超额收益 | 37.279109% | 37.279109% | +0.000000个百分点 |
| 平均换手率 | 3.228094% | 3.228094% | +0.000000个百分点 |

所选配置：

```json
{
  "top_ensemble_name": "lgb1_xgb1_two0_gru1",
  "ensemble_name": "lgb1_xgb1_two1_gru2.25",
  "top_slow_weight": 0.24,
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
  "membership_memory": 0.025,
  "diverse_augmentation": {
    "membership": {
      "model": "rank64_e32",
      "weight": 0.005,
      "blend": "score"
    },
    "top": {
      "model": "pair_rank128_e32",
      "weight": 0.35,
      "blend": "rank"
    },
    "rest": {
      "model": "rank512_e32",
      "weight": 0.2,
      "blend": "rank"
    }
  },
  "secondary_augmentation": {
    "membership": {
      "model": "rank512_seed17_e32",
      "weight": 0.025,
      "blend": "rank"
    },
    "top": {
      "model": "rank512_seed18_e64",
      "weight": 0.025,
      "blend": "rank"
    },
    "rest": {
      "model": "csrank256_e32",
      "weight": 0.15,
      "blend": "score"
    }
  },
  "standalone": null,
  "final_augmentation": {
    "membership": {
      "model": "tail_bce128_e32",
      "weight": 0.0125
    },
    "top": {
      "model": "none",
      "weight": 0.0,
      "regime": "return_dispersion",
      "low": 0.2,
      "high": 0.0
    },
    "rest": {
      "model": "rank512_seed18_e64",
      "weight": 0.125,
      "regime": "return_dispersion",
      "low": 0.0,
      "high": 0.1
    }
  },
  "final_limit_delta": 0.0,
  "standalone_replacement": false,
  "linear_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "return_ridge_l1",
      "weight": 0.025
    }
  },
  "linear_limit_delta": -0.02
}
```

采用2020—2024逐年向前验证，连接1,212日、5,635,800行，年度边界换手连续计算。基准逐元素复现、成熟过去标签收益映射、实际验证CSV官方评分、所选方法标签置空和日期前缀检查、模型重载、预测重放、CSV键值及秩检查均通过。基础模型重新训练：False。

本轮未读取测试标签、未打新测试分；各验证年份此前均已查看，反复选模偏差未校正。候选单独保存于 `candidates/optimization_20261003_r29/submission.csv`，正式交付指针和历史候选保留。逐条评分见同目录的 `optimization_ranking_20261003_r29.json`。
