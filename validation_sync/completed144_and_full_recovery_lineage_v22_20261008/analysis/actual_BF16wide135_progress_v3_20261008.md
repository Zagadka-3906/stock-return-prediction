# 当前优化进度

更新时间：2026-10-08T16:28:28；截止时间：2026-10-10T23:59:00+08:00。

完整合格最佳：第136轮，官方连续验证S=0.451162337656；完整榜13,878条。

新宽网络：已完成6/6个年度；已完成年度：2020,2021,2022,2023,2024,2025。

当前训练：{"status": "actual_mature_annual_BF16_fit", "year": 2025, "at_local": "2026-10-08T12:11:20", "completed_annual_models": 5, "training_rows": 6754006, "checkpoint_path": "E:\\赛题五_本机临时\\neural_BF16_micro8192_bank6_v2_20261008\\2025\\checkpoint.joblib"}

当前周期：{"year": 2025, "completed_epoch": 32, "total_epochs": 32, "saved_epoch": 32, "fit_seconds": 204.594, "training_loss": 0.0814088056542, "training_loss_is_not_validation_score": true}

第135轮评分：{"completed_records": 40, "expected_records": 40, "best_score": 0.45114695864085175, "full135_qualified": true}

后续顺序：六年度训练 → 五年度独立GPU推理 → 37项CDF/111冷前缀 → 三组历史原生检查 → 40项官方评分 → 选中方案冻结与推理 → 完整榜QA46 → GitHub main。

实际服务：
- actual_neural_BF16_micro8192_bank6_v2_20261008：passed，PID 13560，窗口句柄0。
- BF16_independent_full5_GPU_controls_v2_20261008：passed，PID 21072，窗口句柄0。
- BF16_rank_CDF_actual_full37_controls_v1_20261008：passed，PID 5460，窗口句柄0。
- BF16_complete_parent_actual_historical_native_hook3_v1_20261008：passed，PID 16684，窗口句柄0。
- actual_BF16wide135_receiver_preflight_main_publication_v1_20261008：passed，PID 14616，窗口句柄0。
- BF16wide40_round135_source_admission_v3_20261008：无终态记录，PID 9412，窗口句柄0。
- BF16wide40_controls_main_publication_v3_20261008：无终态记录，PID 20252，窗口句柄0。
- BF16wide40_official_comparison_v3_20261008：无终态记录，PID 28996，窗口句柄0。
- BF16wide40_scores_main_publication_v3_20261008：无终态记录，PID 14016，窗口句柄0。
- BF16wide40_selected_candidate_preparation_v3_20261008：无终态记录，PID 20436，窗口句柄0。
- BF16wide40_selected_candidate_sealing_v3_20261008：无终态记录，PID 9620，窗口句柄0。
- BF16wide40_round135_full_registration_v3_20261008：无终态记录，PID 2284，窗口句柄0。

可用空间：D盘1.23 GiB；E盘143.82 GiB。

尚未证明全局优化穷尽；训练损失不能替代验证分数。
