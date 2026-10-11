"""Immutable checkpoint of actual10 Huber fits and completed controls; preserve all unfinished goal work."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    pointer_names=['actual_nonflag_HuberIRLS64_small_location_v2_20261008.json',
        'actual_nonflag_HuberIRLS64_actual200k_location_v1_20261008.json','actual_nonflag_HuberIRLS64_bank10_location_v1_20261008.json',
        'actual_HuberIRLS64_49_parent134_location_v2_20261008.json','actual_HuberIRLS64_18_native_hooks_location_v2_20261008.json',
        'actual_HuberIRLS64_10_causal_inputs_location_v1_20261008.json']
    sources=[Path(__file__),A/'nonflag_HuberIRLS64_bank10_plan_v1_20261008.json',A/'HuberIRLS64_52_round137_plan_v2_20261008.json',
        A/'CrossFamily94_prospective_routes_v2_20261008.json',A/'CrossFamily136_complete_hidden_launches_v2_20261008.json',
        A/'BF16wide135_complete_hidden_launches_v4_20261008.json',A/'CrossFamily136_receiver_preflight_main_v2_20261008/receipt.json',
        A/'actual_HuberIRLS64_bounded_pipeline_hidden_launches_v2_20261008.json',
        A/'actual_HuberIRLS64_bounded_pipeline_hidden_launches_v2_20261008.json',
        A/'actual_HuberIRLS64_bank10_hidden_launch_v1_20261008.json',A/'actual_HuberIRLS64_causal_inputs_hidden_launch_v1_20261008.json',
        A/'nonflag_HuberIRLS64_controls_main_v1_20261008/probe/receipt.json',A/'nonflag_HuberIRLS64_controls_main_v1_20261008/bank/receipt.json',
        A/'HuberIRLS64_historical_controls_main_v2_20261008/receipt.json',A/'actual_user_submission_deadline_and_priority_20261008.json']
    proofs={}
    for filename in pointer_names:
        pointer_path=A/filename;pointer=read(pointer_path);path=Path(pointer['output'])/'verification.json'
        assert sha(path)==pointer['verification_sha256'];proofs[filename]=read(path);sources.extend((pointer_path,path))
    bank=proofs[pointer_names[2]];full=proofs[pointer_names[3]];hooks=proofs[pointer_names[4]];causal=proofs[pointer_names[5]]
    assert bank['actual_native_fits']==10 and (full['actual_full_cases'],full['actual_cold_cases'])==(49,147)
    assert (hooks['actual_hooks'],hooks['actual_cold_hooks'])==(18,18)
    assert (causal['actual_own_window_maturity_controls'],causal['actual_future_training_label_poison_controls'])==(5,10)
    progress=read(A/'actual_neural135_CrossFamily136_progress_v3_20261008.json')
    names=['actual_neural_BF16_micro8192_bank6_v2_20261008','nonflag_HuberIRLS64_actual_bank10_v1_20261008',
        'HuberIRLS64_49_parent134_historical_controls_v2_20261008','HuberIRLS64_18_native_historical_hooks_v2_20261008',
        'HuberIRLS64_10_causal_input_controls_v1_20261008','HuberIRLS64_49_current_parent_controls_v2_20261008']
    services={}
    for name in names:
        folder=A/'service_owned_workflows_20261006'/name;path=folder/'native_launch.json';row=read(path)
        services[name]={'identity':row,'live':owned(row),'terminal':read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None};sources.append(path)
    pins={str(path):sha(path) for path in dict.fromkeys(sources)}
    output=A/'actual_optimization_handoff_v6_20261008.json'
    state={'status':'active_neural135_complete136_queue_and_actual10_Huber_bank49CDF18hooks10poison_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00',
        'current_live_progress_snapshot':progress,'actual_services_at_checkpoint':services,'input_sha256':pins,
        'Huber_actual_controls':{'full_own_mature_models':10,'full_5635800_row_OOF_heads':2,'full_parent134_CDF_cases':49,
            'cold_CDF_cases':147,'historical_native_hooks':18,'cold_native_hooks':18,'independent_maturity_windows':5,
            'later_training_label_poison_controls':10,'actual_quality_scores':0,'actual_future_candidate_inferences':0},
        'Huber_main_receipts':{phase:read(A/'nonflag_HuberIRLS64_controls_main_v1_20261008'/phase/'receipt.json') for phase in ('probe','bank')},
        'Huber_historical_main_receipt':read(A/'HuberIRLS64_historical_controls_main_v2_20261008/receipt.json'),
        'still_required135':['Finish2023-2025 own-mature32-epoch BF16 fits; do not restart completed2020-2022.',
            'Queued actual5 GPU oracles,37 CDF111cold,3 historical hooks,40 original official comparisons and scores main.',
            'Frozen selected full graph/source/calibration; two future native/independent replays and cold80 or honest exact anchor reuse.',
            'Original six-view45second QA46 complete board and actual main receipt.'],
        'still_required136':['Current8-service queue2 already live; wait complete135 then qualified exact complete parent controls.',
            '94 original official comparisons, all8 metrics, selected freeze and actual future candidate controls or exact anchor reuse.',
            'Original six-view45second QA47 complete board and actual main receipt.'],
        'still_required137':['52-case plan2 frozen:134135136 anchors, identity,48 signed-Huber configurations.',
            'Current-parent49/147 receiver2 is live and waits complete136 QA47/main plus historical controls main.',
            'Prepare all source-admission, scoring, selected prep/seal, registration/fullQA48, main and24 prospective receivers before first137 quality score.',
            'Preserve complete signed-Bayes, optional BF16 and CrossFamily parent graphs; expected physical model counts use uniqueSHA union.',
            'Use D regular original-scope scoring_validation_only directories; large outputs E and hash-verified cross-volume transfers.',
            'Three future backend injections compiled only: actual1599600x2 native/independent and cold80 not yet claimed.',
            'All52 original official comparisons; exact8-metric qualification, freeze, candidate, QA48 and fullboard main still required.'],
        'remaining_uncovered_directions_with_no_exhaustion_claim':['Negative direction of the NEW own-mature BF16 bank after full GPU controls; no extra GPU fits needed.',
            'Potential Huber+Ridge/RFF/Bayes mixtures after current pure signed-Huber validation; not yet predeclared or scored.'],
        'old135_queues1_2_3_and_expired_Oct7_stop_guards_not_to_be_restarted':True,
        'large_models_feature_caches_and_new_temporaries_on_D_or_E_only':True,'current_active_release_not_changed':True,
        'goal_active_not_paused_complete_or_blocked':True,'global_optimization_or_resource_exhaustion_not_proven':True,
        'test_labels_read':False}
    create(output,state)
    for path,digest in pins.items():assert sha(path)==digest,path
    lines=['# 实际优化交接 v6','',f"记录时间：{state['at_local']}；截止：2026年10月10日23:59（UTC+8）。",'',
        f"当前完整合格最佳：第{progress['best_fully_qualified']['round']}轮，S={progress['best_fully_qualified']['official_score']:.12f}；完整榜{progress['latest_fully_qualified']['connected_records']:,}条。",'',
        f"神经年度完成{len(progress['annual_models_complete'])}/6；135、136轮仍按既有完整队列执行。",'',
        '新增Huber：10个完整年度模型、两组5635800行OOF；49完整CDF/147冷前缀、18原生接入/18冷接入、5个独立成熟窗口和10个后续训练标签扰动检查通过。没有新的Huber官方分或测试推理。','',
        '第137轮计划已固定52项；接收器、官方评分、冻结、完整候选复核和QA48尚需完成，不能登记为合格轮次。','',
        '下一步首先补齐第137轮完整流程与24个前置接收器检查；保持135/136队列和GPU训练运行。已有检查记录同步main。','',
        '还有未覆盖的负向新神经残差和Huber跨模型集成方向，不能宣布优化穷尽。过期停工任务不恢复。','']
    target=A/'actual_optimization_handoff_v6_20261008.md';assert not target.exists();target.write_text('\n'.join(lines),encoding='utf8',newline='\n')
    print('Immutable actual optimization handoff6 written; goal remains active.',flush=True)


if __name__=='__main__':main()
