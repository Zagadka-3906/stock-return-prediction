# 第51轮：固定折点加性岭回归的完整方案用途融合

本轮完成188种不同输出配置、196条评分记录。R50基准 **0.450912800391**，最高连续验证分 **0.450912800391**，未获得提升，最高分仍由原方案取得。

| 阶段 | 评分记录 | 截至阶段结束的最高分 | 相比前阶段变化 |
| --- | ---: | ---: | ---: |
| 全部模型分用途独立对照 | 145 | 0.450912800 | +0.000000000 |
| 最佳单用途模型组合 | 8 | 0.450912800 | +0.000000000 |
| 新用途权重顺序细搜 | 18 | 0.450912800 | +0.000000000 |
| 新成员留存与涨停偏移细搜 | 25 | 0.450912800 | +0.000000000 |

具体方法的起点和自适应细搜规则已在评分前冻结。累计最高分是选模过程记录，阶段差异不表示独立因果贡献；重复基准不计作新的模型训练。

本轮评分记录中，164次重新调用官方评分，32次复用完全相同CSV及验证输入的已有官方结果。CSV、验证数据、评分代码和运行库版本共同确定缓存；对应证据已随选定方案冻结。



| 指标 | R50基准 | 本轮选中方案 | 变化 |
| --- | ---: | ---: | ---: |
| Rank IC | 0.121756177 | 0.121756177 | +0.000000000 |
| 年化超额收益 | 37.300598% | 37.300598% | +0.000000个百分点 |
| 平均换手率 | 3.230488% | 3.230488% | +0.000000个百分点 |

所选配置：

```json
{
  "top_ensemble_name": "lgb1_xgb1_two0_gru1",
  "ensemble_name": "lgb1_xgb1_two1_gru2.25",
  "top_slow_weight": 0.265,
  "slow16_weight": 0.255,
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
      "weight": 0.125,
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
      "weight": 0.175,
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
      "weight": 0.15,
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
  "linear_limit_delta": -0.02,
  "regularization_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "rank512_drop000_e32",
      "weight": 0.025
    }
  },
  "regularization_limit_delta": 0.0,
  "stacking_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "none",
      "weight": 0.0
    }
  },
  "stacking_limit_delta": 0.0,
  "neural_tuning_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "rank512_o05_lr0005_e32",
      "weight": 0.037500000000000006
    }
  },
  "neural_tuning_limit_delta": 0.0,
  "catboost_tuning_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "cat_rank10_e600",
      "weight": 0.2
    }
  },
  "catboost_tuning_limit_delta": -0.02,
  "expanded_stacking_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "none",
      "weight": 0.0
    }
  },
  "expanded_stacking_limit_delta": 0.0,
  "additive_ridge_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "none",
      "weight": 0.0
    }
  },
  "additive_ridge_limit_delta": 0.0,
  "fourier_ridge_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "none",
      "weight": 0.0
    }
  },
  "fourier_ridge_limit_delta": 0.0,
  "nonlinear_stacking_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "none",
      "weight": 0.0
    }
  },
  "nonlinear_stacking_limit_delta": 0.0,
  "fourier_tuning_augmentation": {
    "membership": {
      "model": "none",
      "weight": 0.0
    },
    "top": {
      "model": "none",
      "weight": 0.0
    },
    "rest": {
      "model": "none",
      "weight": 0.0
    }
  },
  "fourier_tuning_limit_delta": 0.0,
  "temporal_postprocessing": {
    "alpha": 0.97,
    "mix": 0.0,
    "power": 1.0
  },
  "whole_scheme_graph": {
    "through_round": 49,
    "root": {
      "kind": "complete_r30",
      "round": 30,
      "configuration": {
        "wave": 147,
        "arm": "slow16_weight_2_0.025",
        "top_ensemble_name": "lgb1_xgb1_two0_gru1",
        "ensemble_name": "lgb1_xgb1_two1_gru2.25",
        "top_slow_weight": 0.265,
        "slow16_weight": 0.255,
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
            "weight": 0.1375,
            "blend": "rank"
          }
        },
        "secondary_augmentation": {
          "membership": {
            "model": "rank512_seed17_e32",
            "weight": 0.0,
            "blend": "rank"
          },
          "top": {
            "model": "rank512_seed18_e64",
            "weight": 0.025,
            "blend": "rank"
          },
          "rest": {
            "model": "csrank256_e32",
            "weight": 0.19999999999999998,
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
            "weight": 0.1625,
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
            "weight": 0.037500000000000006
          }
        },
        "linear_limit_delta": -0.02,
        "donor": "baseline",
        "ensemble_weights": {
          "lgb": 1.0,
          "xgb": 1.0,
          "two": 1.0,
          "gru": 2.25
        },
        "top_ensemble_weights": {
          "lgb": 1.0,
          "xgb": 1.0,
          "gru": 1.0
        },
        "membership_ensemble_weights": {
          "lgb": 0.75,
          "xgb": 1.0,
          "two": 1.0,
          "gru": 2.25
        },
        "role_ensembles_split": true,
        "fold_local_pruning_repaired": true,
        "pruned_member_excluded": true,
        "connected_final_score": 0.4508028811246302,
        "metrics": {
          "ic_mean": 0.12158028352662809,
          "ic_std": 0.11064034616811237,
          "icir": 1.0988783724690543,
          "ic_positive_ratio": 0.8910891089108911,
          "annual_excess": 0.37285731556999197,
          "top1_annual_ret": 0.39835106963024947,
          "mean_turnover": 0.032288089856728916,
          "final_score": 0.4508028811246302
        },
        "construction": {
          "foundation": {
            "days": 1212,
            "m_frac": 0.984,
            "retention": null,
            "boundary_tie_days": 0,
            "eligibility_limited_days": 187,
            "swaps": 93109,
            "mean_retention_ratio": 0.9836875764424351
          },
          "final_augmentation": {
            "extra_role_augmentation": true,
            "second_retention": 0.984,
            "construction": {
              "days": 1212,
              "m_frac": 0.984,
              "retention": null,
              "boundary_tie_days": 0,
              "eligibility_limited_days": 187,
              "swaps": 3842,
              "mean_retention_ratio": 0.9835701857477712
            },
            "additional_limit_shift": 0.0
          },
          "linear_augmentation": {
            "extra_role_augmentation": true,
            "second_retention": 0.0,
            "construction": {
              "days": 1212,
              "m_frac": 0.0,
              "retention": null,
              "boundary_tie_days": 0,
              "eligibility_limited_days": 0,
              "swaps": 0,
              "mean_retention_ratio": 0.9835701857477712
            },
            "additional_limit_shift": -0.02
          }
        },
        "official_score_cache": {
          "cache_hit": false,
          "cache_key": "f9cce5ec64b7be3cf6fc0459fafe146c08a2853749ba561dbbbd74438f99c0ab",
          "official_metrics_source": "D:\\3.Study\\数据分析\\赛题五\\analysis\\optimization_20261003_r30\\parallel_official_workers\\worker_1\\identical_official_scores\\f9cce5ec64b7be3cf6fc0459fafe146c08a2853749ba561dbbbd74438f99c0ab.json"
        },
        "causal_return_mapping": {
          "actual_return_mapped_csv_scored": true,
          "within_day_ranks_bit_identical": true,
          "boundaries": [
            {
              "year": 2020,
              "mapping_last_label_date": 20191230,
              "exclusive_cutoff": 20191231,
              "method": "prevalidation training moments affine fallback"
            },
            {
              "year": 2021,
              "mapping_last_label_date": 20201230,
              "exclusive_cutoff": 20201231,
              "method": "past mature OOF isotonic"
            },
            {
              "year": 2022,
              "mapping_last_label_date": 20211230,
              "exclusive_cutoff": 20211231,
              "method": "past mature OOF isotonic"
            },
            {
              "year": 2023,
              "mapping_last_label_date": 20221229,
              "exclusive_cutoff": 20221230,
              "method": "past mature OOF isotonic"
            },
            {
              "year": 2024,
              "mapping_last_label_date": 20231228,
              "exclusive_cutoff": 20231229,
              "method": "past mature OOF isotonic"
            }
          ],
          "test_labels_read": false,
          "cross_round_identical_official_reuse": {
            "cross_round_cache_hit": false
          }
        },
        "parallel_execution": {
          "worker_slot": 1,
          "worker_pid": 43496,
          "private_scoring_directory": "D:\\3.Study\\数据分析\\赛题五\\analysis\\optimization_20261003_r30\\parallel_official_workers\\worker_1\\scoring_validation_only",
          "same_declared_configuration": true
        }
      }
    },
    "layers": [
      {
        "name": "regularization",
        "round": 31,
        "group": "regularization_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "rank512_drop000_e32",
            "weight": 0.025
          }
        },
        "retention": 0.984,
        "original_delta": 0.05499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "stacking",
        "round": 33,
        "group": "stacking_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.05499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "neural_tuning",
        "round": 35,
        "group": "neural_tuning_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "rank512_o05_lr0005_e32",
            "weight": 0.037500000000000006
          }
        },
        "retention": 0.984,
        "original_delta": 0.05499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "catboost_tuning",
        "round": 37,
        "group": "catboost_tuning_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "cat_rank10_e600",
            "weight": 0.2
          }
        },
        "retention": 0.984,
        "original_delta": 0.05499999999999999,
        "additional_delta": -0.02
      },
      {
        "name": "expanded_stacking",
        "round": 39,
        "group": "expanded_stacking_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "additive_ridge",
        "round": 41,
        "group": "additive_ridge_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "fourier_ridge",
        "round": 43,
        "group": "fourier_ridge_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "nonlinear_stacking",
        "round": 45,
        "group": "nonlinear_stacking_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "fourier_tuning",
        "round": 47,
        "group": "fourier_tuning_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      }
    ],
    "temporal_postprocessing": {
      "alpha": 0.97,
      "mix": 0.0,
      "power": 1.0
    },
    "discarded_branches": [],
    "active_weight_axes": [
      {
        "round": 30,
        "group": "diverse_augmentation",
        "role": "membership",
        "model": "rank64_e32",
        "anchor": 0.005
      },
      {
        "round": 30,
        "group": "diverse_augmentation",
        "role": "top",
        "model": "pair_rank128_e32",
        "anchor": 0.35
      },
      {
        "round": 30,
        "group": "diverse_augmentation",
        "role": "rest",
        "model": "rank512_e32",
        "anchor": 0.125
      },
      {
        "round": 30,
        "group": "secondary_augmentation",
        "role": "membership",
        "model": "rank512_seed17_e32",
        "anchor": 0.025
      },
      {
        "round": 30,
        "group": "secondary_augmentation",
        "role": "top",
        "model": "rank512_seed18_e64",
        "anchor": 0.025
      },
      {
        "round": 30,
        "group": "secondary_augmentation",
        "role": "rest",
        "model": "csrank256_e32",
        "anchor": 0.175
      },
      {
        "round": 30,
        "group": "final_augmentation",
        "role": "membership",
        "model": "tail_bce128_e32",
        "anchor": 0.0125
      },
      {
        "round": 30,
        "group": "final_augmentation",
        "role": "rest",
        "model": "rank512_seed18_e64",
        "anchor": 0.15
      },
      {
        "round": 30,
        "group": "linear_augmentation",
        "role": "rest",
        "model": "return_ridge_l1",
        "anchor": 0.025
      },
      {
        "round": 31,
        "group": "regularization_augmentation",
        "role": "rest",
        "model": "rank512_drop000_e32",
        "anchor": 0.025
      },
      {
        "round": 35,
        "group": "neural_tuning_augmentation",
        "role": "rest",
        "model": "rank512_o05_lr0005_e32",
        "anchor": 0.037500000000000006
      },
      {
        "round": 37,
        "group": "catboost_tuning_augmentation",
        "role": "rest",
        "model": "cat_rank10_e600",
        "anchor": 0.2
      }
    ],
    "each_layer_uses_its_own_historical_retention": true
  },
  "basis_role_scheme_graph": {
    "through_round": 51,
    "root": {
      "kind": "complete_r30",
      "round": 30,
      "configuration": {
        "wave": 147,
        "arm": "slow16_weight_2_0.025",
        "top_ensemble_name": "lgb1_xgb1_two0_gru1",
        "ensemble_name": "lgb1_xgb1_two1_gru2.25",
        "top_slow_weight": 0.265,
        "slow16_weight": 0.255,
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
            "weight": 0.1375,
            "blend": "rank"
          }
        },
        "secondary_augmentation": {
          "membership": {
            "model": "rank512_seed17_e32",
            "weight": 0.0,
            "blend": "rank"
          },
          "top": {
            "model": "rank512_seed18_e64",
            "weight": 0.025,
            "blend": "rank"
          },
          "rest": {
            "model": "csrank256_e32",
            "weight": 0.19999999999999998,
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
            "weight": 0.1625,
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
            "weight": 0.037500000000000006
          }
        },
        "linear_limit_delta": -0.02,
        "donor": "baseline",
        "ensemble_weights": {
          "lgb": 1.0,
          "xgb": 1.0,
          "two": 1.0,
          "gru": 2.25
        },
        "top_ensemble_weights": {
          "lgb": 1.0,
          "xgb": 1.0,
          "gru": 1.0
        },
        "membership_ensemble_weights": {
          "lgb": 0.75,
          "xgb": 1.0,
          "two": 1.0,
          "gru": 2.25
        },
        "role_ensembles_split": true,
        "fold_local_pruning_repaired": true,
        "pruned_member_excluded": true,
        "connected_final_score": 0.4508028811246302,
        "metrics": {
          "ic_mean": 0.12158028352662809,
          "ic_std": 0.11064034616811237,
          "icir": 1.0988783724690543,
          "ic_positive_ratio": 0.8910891089108911,
          "annual_excess": 0.37285731556999197,
          "top1_annual_ret": 0.39835106963024947,
          "mean_turnover": 0.032288089856728916,
          "final_score": 0.4508028811246302
        },
        "construction": {
          "foundation": {
            "days": 1212,
            "m_frac": 0.984,
            "retention": null,
            "boundary_tie_days": 0,
            "eligibility_limited_days": 187,
            "swaps": 93109,
            "mean_retention_ratio": 0.9836875764424351
          },
          "final_augmentation": {
            "extra_role_augmentation": true,
            "second_retention": 0.984,
            "construction": {
              "days": 1212,
              "m_frac": 0.984,
              "retention": null,
              "boundary_tie_days": 0,
              "eligibility_limited_days": 187,
              "swaps": 3842,
              "mean_retention_ratio": 0.9835701857477712
            },
            "additional_limit_shift": 0.0
          },
          "linear_augmentation": {
            "extra_role_augmentation": true,
            "second_retention": 0.0,
            "construction": {
              "days": 1212,
              "m_frac": 0.0,
              "retention": null,
              "boundary_tie_days": 0,
              "eligibility_limited_days": 0,
              "swaps": 0,
              "mean_retention_ratio": 0.9835701857477712
            },
            "additional_limit_shift": -0.02
          }
        },
        "official_score_cache": {
          "cache_hit": false,
          "cache_key": "f9cce5ec64b7be3cf6fc0459fafe146c08a2853749ba561dbbbd74438f99c0ab",
          "official_metrics_source": "D:\\3.Study\\数据分析\\赛题五\\analysis\\optimization_20261003_r30\\parallel_official_workers\\worker_1\\identical_official_scores\\f9cce5ec64b7be3cf6fc0459fafe146c08a2853749ba561dbbbd74438f99c0ab.json"
        },
        "causal_return_mapping": {
          "actual_return_mapped_csv_scored": true,
          "within_day_ranks_bit_identical": true,
          "boundaries": [
            {
              "year": 2020,
              "mapping_last_label_date": 20191230,
              "exclusive_cutoff": 20191231,
              "method": "prevalidation training moments affine fallback"
            },
            {
              "year": 2021,
              "mapping_last_label_date": 20201230,
              "exclusive_cutoff": 20201231,
              "method": "past mature OOF isotonic"
            },
            {
              "year": 2022,
              "mapping_last_label_date": 20211230,
              "exclusive_cutoff": 20211231,
              "method": "past mature OOF isotonic"
            },
            {
              "year": 2023,
              "mapping_last_label_date": 20221229,
              "exclusive_cutoff": 20221230,
              "method": "past mature OOF isotonic"
            },
            {
              "year": 2024,
              "mapping_last_label_date": 20231228,
              "exclusive_cutoff": 20231229,
              "method": "past mature OOF isotonic"
            }
          ],
          "test_labels_read": false,
          "cross_round_identical_official_reuse": {
            "cross_round_cache_hit": false
          }
        },
        "parallel_execution": {
          "worker_slot": 1,
          "worker_pid": 43496,
          "private_scoring_directory": "D:\\3.Study\\数据分析\\赛题五\\analysis\\optimization_20261003_r30\\parallel_official_workers\\worker_1\\scoring_validation_only",
          "same_declared_configuration": true
        }
      }
    },
    "layers": [
      {
        "name": "regularization",
        "round": 31,
        "group": "regularization_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "rank512_drop000_e32",
            "weight": 0.025
          }
        },
        "retention": 0.984,
        "original_delta": 0.05499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "stacking",
        "round": 33,
        "group": "stacking_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.05499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "neural_tuning",
        "round": 35,
        "group": "neural_tuning_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "rank512_o05_lr0005_e32",
            "weight": 0.037500000000000006
          }
        },
        "retention": 0.984,
        "original_delta": 0.05499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "catboost_tuning",
        "round": 37,
        "group": "catboost_tuning_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "cat_rank10_e600",
            "weight": 0.2
          }
        },
        "retention": 0.984,
        "original_delta": 0.05499999999999999,
        "additional_delta": -0.02
      },
      {
        "name": "expanded_stacking",
        "round": 39,
        "group": "expanded_stacking_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "additive_ridge",
        "round": 41,
        "group": "additive_ridge_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "fourier_ridge",
        "round": 43,
        "group": "fourier_ridge_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "nonlinear_stacking",
        "round": 45,
        "group": "nonlinear_stacking_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "fourier_tuning",
        "round": 47,
        "group": "fourier_tuning_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.984,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      },
      {
        "name": "additive_basis",
        "round": 51,
        "group": "additive_basis_augmentation",
        "specs": {
          "membership": {
            "model": "none",
            "weight": 0.0
          },
          "top": {
            "model": "none",
            "weight": 0.0
          },
          "rest": {
            "model": "none",
            "weight": 0.0
          }
        },
        "retention": 0.0,
        "original_delta": 0.03499999999999999,
        "additional_delta": 0.0
      }
    ],
    "temporal_postprocessing": {
      "alpha": 0.97,
      "mix": 0.0,
      "power": 1.0
    },
    "discarded_branches": [],
    "active_weight_axes": [
      {
        "round": 30,
        "group": "diverse_augmentation",
        "role": "membership",
        "model": "rank64_e32",
        "anchor": 0.005
      },
      {
        "round": 30,
        "group": "diverse_augmentation",
        "role": "top",
        "model": "pair_rank128_e32",
        "anchor": 0.35
      },
      {
        "round": 30,
        "group": "diverse_augmentation",
        "role": "rest",
        "model": "rank512_e32",
        "anchor": 0.125
      },
      {
        "round": 30,
        "group": "secondary_augmentation",
        "role": "membership",
        "model": "rank512_seed17_e32",
        "anchor": 0.025
      },
      {
        "round": 30,
        "group": "secondary_augmentation",
        "role": "top",
        "model": "rank512_seed18_e64",
        "anchor": 0.025
      },
      {
        "round": 30,
        "group": "secondary_augmentation",
        "role": "rest",
        "model": "csrank256_e32",
        "anchor": 0.175
      },
      {
        "round": 30,
        "group": "final_augmentation",
        "role": "membership",
        "model": "tail_bce128_e32",
        "anchor": 0.0125
      },
      {
        "round": 30,
        "group": "final_augmentation",
        "role": "rest",
        "model": "rank512_seed18_e64",
        "anchor": 0.15
      },
      {
        "round": 30,
        "group": "linear_augmentation",
        "role": "rest",
        "model": "return_ridge_l1",
        "anchor": 0.025
      },
      {
        "round": 31,
        "group": "regularization_augmentation",
        "role": "rest",
        "model": "rank512_drop000_e32",
        "anchor": 0.025
      },
      {
        "round": 35,
        "group": "neural_tuning_augmentation",
        "role": "rest",
        "model": "rank512_o05_lr0005_e32",
        "anchor": 0.037500000000000006
      },
      {
        "round": 37,
        "group": "catboost_tuning_augmentation",
        "role": "rest",
        "model": "cat_rank10_e600",
        "anchor": 0.2
      }
    ],
    "each_layer_uses_its_own_historical_retention": true
  }
}
```

采用2020—2024逐年向前验证，连接1,212日、5,635,800行，年度边界换手连续计算。基准逐元素复现、成熟过去标签收益映射、实际验证CSV官方评分、所选方法标签置空和日期前缀检查、模型重载、预测重放、CSV键值及秩检查均通过。基础模型重新训练：False。

本轮未读取测试标签、未打新测试分；各验证年份此前均已查看，反复选模偏差未校正。候选单独保存于 `candidates/optimization_20261003_r51/submission.csv`，正式交付指针和历史候选保留。逐条评分见同目录的 `optimization_ranking_20261003_r51.json`。
