# 最新用户指令（2026-10-10）

用户已明确要求现在恢复模型优化，优化截止时间更改为 **2026-10-11 11:00（Asia/Taipei，UTC+08:00）**。此前即时停工和10月9日23:55安排已被取代。截止前持续优化，优先复用已核实的年度模型、epoch检查点和原始评分缓存，节省计算时间。

每轮开始及启动训练、评分、推理或发布前，读取 `analysis/current_user_runtime_control_20261010.json`、兼容09控制文件和本机时间。只启动已有授权范围内的工作。新守护记录在 `analysis/user_requested_stop1100_until_manual_continue_v1_20261011/actual_schedule_activation.json`；禁止重启旧守护。实际截止为10月11日11:00，到时停止项目任务，保存恢复清单，依据本次明确用户截止请求暂停目标。未完成年度训练或评分不得记为完成。

# 历史用户停工安排（已被上述最新指令取代）

用户明确要求 **2026-10-09 23:55（Asia/Taipei，UTC+08:00）停止工作**，此后等用户实际发送“继续”再恢复。

- 每轮目标续行开始时，以及启动新训练、评分、推理或发布前，读取 `analysis/current_user_runtime_control_20261009.json` 与本机时间。兼容入口 `analysis/current_user_runtime_control_20261008.json` 也已同步当天安排。
- 截止时间到达前继续优化，保持目标 active；不得因为设置定时停工而提前将目标 paused。
- 已启动隐藏停工守护程序，记录在 `analysis/user_requested_stop2355_until_manual_continue_v1_20261009/actual_schedule_activation.json`。23:53收拢空闲派发与发布，23:55冻结并停止已核实归属的本项目任务，保存恢复清单。不要终止或重复启动这个守护程序。
- 时间到达后停止优化，不启动新的任务、不自动重启已停止任务。检查 `guardian_status.json` 与 `disk_recovery_manifest.json`；若当前目标仍 active，依据用户这次明确请求调用 `update_goal(status="paused")` 并报告状态。自动目标续行不属于用户的“继续”。
- 次日收到用户实际“继续”后，可以恢复。先核对恢复清单和已落盘文件，更新两个运行控制文件为明确手动恢复；过期的10月9日停工安排不得沿用到新的一天。中断任务只能从已核实检查点恢复或建立新尝试，不得盲目重跑排他输出路径。
- 停工保留已完成的分数、候选、提交文件、GitHub main回执及完整年度模型/已完成epoch检查点；不把未完成的年度训练或评分记为完成。

该文件仅记录本次用户停工指令；用户后续的明确指令优先。
