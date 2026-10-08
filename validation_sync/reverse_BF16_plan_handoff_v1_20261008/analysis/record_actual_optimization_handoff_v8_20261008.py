"""Record live calendar-safe queues and the newly frozen reverse-neural direction honestly."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    progress=read(A/'actual_neural135_CrossFamily136_progress_v5_20261008.json')
    receipt=A/'multiyear136137_recovery_main_v2_20261008/receipt.json';assert read(receipt)['status']=='pushed_and_remote_head_verified'
    sources=[Path(__file__),receipt,A/'actual_user_submission_deadline_and_priority_20261008.json',
        A/'BF16wide135_complete_hidden_launches_v4_20261008.json',A/'CrossFamily136_complete_hidden_launches_v4_20261008.json',
        A/'Huber137_complete_hidden_launches_v3_20261008.json',A/'actual_multiyear136137_recovered_queue_launches_v2_20261008.json',
        A/'actual_multiyear_residual_calendar_location_v1_20261008.json',A/'actual_CrossFamily15_native_hooks_location_v2_20261008.json',
        A/'actual_HuberIRLS64_18_native_hooks_location_v3_20261008.json',A/'multiyear136137_queue_recovery_v2_20261008.json',
        A/'BF16reverse40_round138_plan_v1_20261008.json',A/'BF16_reverse_rank_CDF_synthetic_preflight_v1_20261008/verification.json',
        A/'BF16_reverse_native_receiver_preparation_v1_20261008.json',A/'actual_BF16reverse40_plan_and_full37_hidden_launch_v1_20261008.json',
        A/'actual_BF16_reverse_historical_native_hook3_hidden_launch_v1_20261008.json',
        A/'monitor_neural135_and_CrossFamily136_v5_20261008.py',A/'actual_optimization135136137_progress_hidden_launch_v5_20261008.json']
    services={}
    for phase,path in zip((135,136,137),sources[3:6]):
        rows=read(path)['launches']
        for name,row in rows.items():
            assert owned(row),name;assert row['actual_native_console_handle']==0
            services[name]={'round':phase,'identity':row,'live':True}
    fitter=A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json'
    assert owned(read(fitter));sources.append(fitter)
    reverse=read(A/'BF16_reverse_rank_CDF_synthetic_preflight_v1_20261008/verification.json')
    assert reverse['actual_cases']==39 and reverse['actual_day_controls']==78 and reverse['actual_quality_scores']==0
    pins={str(p):sha(p) for p in sources};output=A/'actual_optimization_handoff_v8_20261008.json'
    state={'status':'active135v4_136v4_137v3_calendar_safe_and_frozen_reverse_BF16_next_direction',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00',
        'input_sha256':pins,'actual_progress_at_checkpoint':progress,'actual_owned_live_services':services,
        'calendar_controls':{'historical_native_hooks':33,'multiyear_native_cases':33,'day_controls':66,
            'saved_fit_year':2025,'prediction_calendar_years':[2025,2026],'main_receipt':read(receipt),
            'date_remapped_historical_X_only_not_future_qualification':True},
        'still_required135':['Finish2023-2025 full own-mature BF16 fits; retain completed checkpoints.',
            'Full5 independent GPU,37 CDF111cold,3 native hooks;40 original official comparisons and scores main.',
            'Selected whole graph/source/return mapping freeze; two full future native/independent and cold80 or exact anchor reuse.',
            'Original complete six-view45second QA46 and main fullboard receipt.'],
        'still_required136':['Use current service version4, not administratively superseded versions1-3.',
            'Wait complete135, freeze highest-S qualified complete parent and exact91/273 controls.',
            '94 official all8 comparisons, freeze, candidate two full native/independent+cold80 or exact anchor reuse.',
            'Original full six-view45second QA47 and main complete board.'],
        'still_required137':['Use current service version3 and exact-current-parent control version4.',
            'Wait complete136 QA47/main, freeze qualified parent and exact49/147 controls.',
            '52 official all8 comparisons, full graph/source/mapping freeze, actual candidate or exact anchor reuse.',
            'Original six-view45second QA48 and main fullboard.'],
        'still_required138':['Plan1 frozen40 cases: three135136137 anchors,36 reverse-neural roles/weights and identity.',
            '39 synthetic CDF/78 day controls passed; four future-backend compilations are not actual inference.',
            'Queued37 full/111 cold controls and3 actual historical native hooks after qualified137; no extra GPU fits.',
            'Complete source/admission/40-official/selected-prep-seal/registration/QA49/main receivers and their prospective proof still need implementation.',
            'Preserve complete signedBayes, positiveBF16, CrossFamily and Huber parent branches; count unique modelSHA union.',
            'Actual future X only after whole graph/config/Python/calibration frozen; fixed2025 fit across2025/2026.',
            'All40 original all8 metrics, selected two full independent/cold80 or exact anchor reuse and all6 fullboard views.'],
        'other_uncovered_directions':['Huber+Ridge/RFF/Bayes mixtures are not yet predeclared or tested.'],
        'model_selection_bias_uncorrected':True,'global_exhaustion_or_goal_completion_not_claimed':True,
        'old_superseded_receivers_and_expired_Oct7_stop_guards_not_to_be_restarted':True,
        'goal_active_not_paused_complete_or_blocked':True,'large_outputs_on_E_original_scoring_scratch_on_D':True,
        'active_release_unchanged':True,'test_labels_read':False}
    create(output,state)
    target=A/'actual_optimization_handoff_v8_20261008.md';assert not target.exists()
    epoch=progress['latest_actual_epoch'];best=progress['best_fully_qualified']
    lines=['# 实际优化交接 v8','',f"记录时间：{state['at_local']}；截止：2026年10月10日23:59（UTC+8）。",'',
        f"当前完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；完整榜{progress['latest_fully_qualified']['connected_records']:,}条。",'',
        f"神经年度完成{len(progress['annual_models_complete'])}/6；当前{epoch['year']}已保存{epoch['saved_epoch']}/{epoch['total_epochs']}轮。训练损失不是验证分。",'',
        '跨年推理已修正：冻结2025模型用于2025和2026；33历史原生、33跨年、66单日及774完整父图检查通过并上传main。',
        '第135轮服务版本4；第136轮版本4；第137轮版本3、完整父控制版本4。已启动依赖等待、官方评分、选中冻结、候选、完整榜QA及main全流程。尚无135/136/137官方新分。','',
        '第138轮新增负向神经CDF：40项固定计划、39合成和78单日控制通过；无需额外GPU拟合，37完整/111冷前缀和3原生历史检查已排队。完整138接收器和质量验证仍需实现。','',
        '下一步完成138完整流程及前置复核；持续检查GPU年度完成后135→136→137的实际推进。不得重启过期停工守卫或弃用版本。','',
        '当前目标仍在进行，尚无可行方向或计算资源穷尽的证据。新未来推理和合格轮次仅按实际证据登记。','']
    target.write_text('\n'.join(lines),encoding='utf8',newline='\n')
    for p,d in pins.items():assert sha(p)==d,p
    print('Handoff8 records current recovered queues and uncovered reverse-neural work; goal remains active.',flush=True)


if __name__=='__main__':main()
