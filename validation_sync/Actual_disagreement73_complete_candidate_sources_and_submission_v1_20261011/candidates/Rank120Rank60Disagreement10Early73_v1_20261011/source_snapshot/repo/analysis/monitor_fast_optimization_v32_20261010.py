"""Current actual pipelines, compact progress, and complete supplementary score inventory."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys, time, shutil
A = Path(__file__).resolve().parent
sys.path[:0] = [str(A.parent), str(A)]
from run_dependency_queue_v3_20261006 import read, owned
from scheduled_user_pause_20261007 import write

def main():
    import psutil
    while True:
        now = datetime.now(timezone(timedelta(hours=8)))
        c = read(A / 'current_user_runtime_control_20261010.json')
        jobs = {}
        for name in ['actual_fast_neural_frontier228_normalization_queue_v1_20261010','actual_complete_fast_neural_frontier228_main_v28_20261010','FastNeuralFrontier169_selected_native14_v1_20261010','FastNeuralFrontier169_complete228_family_v2_20261010','FastNeuralFrontier169_selected_candidate_preparation_v1_20261010','FastNeuralFrontier169_selected_candidate_sealing_v1_20261010','FastNeuralFrontier169_round169_full_registration_v1_20261010','actual_recent252_rank5_own_controls_and_training_queue_v1_20261010','actual_BF16_medium2048_recent252rank5huber050_seed09_restart_control_v1_20261009','BF16Recent252Rank5Huber050172_independent_small_CPU_v1_20261009','actual_BF16_medium2048_recent252rank5huber050_seed09_e64_bank6_v1_20261009','BF16Recent252Rank5Huber050172_independent_full5_GPU_controls_v1_20261009','BF16Recent252Rank5Huber050172_actual_native42_calendar_v1_20261009','actual_Recent252Rank5_after168_high_impact65_screen_v1_20261010','actual_Recent252Rank5_after168_65_completion_main_v27_20261010','actual_recent252_forward5_own_controls_and_training_queue_v1_20261010','actual_BF16_medium2048_recent252forward5huber050_seed09_restart_control_v1_20261009','BF16Recent252Forward5Huber050171_independent_small_CPU_v1_20261009','actual_BF16_medium2048_recent252forward5huber050_seed09_e64_bank6_v1_20261009','BF16Recent252Forward5Huber050171_independent_full5_GPU_controls_v1_20261009','BF16Recent252Forward5Huber050171_actual_native42_calendar_v1_20261009','actual_Recent252Forward5_after168_high_impact65_screen_v1_20261010','actual_Recent252Forward5_after168_65_completion_main_v26_20261010','actual_E_guard_actual_anchor_and_forward5_CPU_admission_main_v10_20261010','actual_round168_documentation_errata_main_v11_20261010','actual_mean5_full_preparation_and_exact_scratch_cleanup_main_v12_20261010','actual_RecentReturn252_after167_protected_fine31_screen_E_guard_recovery_v3_20261010','actual_Recent252Forward20_after168_high_impact65_screen_E_guard_recovery_v3_20261010','actual_RecentReturn252_after167_protected_fine31_completion_main_v23_20261010','actual_Recent252Forward20_after168_high_impact65_completion_main_v24_20261010','ReturnProtected167_round167_full_registration_cross_volume_recovery_v4_20261010', 'ReturnProtected167_selected_native14_v1_20261010', 'ReturnProtected167_selected_candidate_preparation_v1_20261010', 'ReturnProtected167_selected_candidate_sealing_v1_20261010', 'ReturnProtected167_round167_full_registration_v1_20261010', 'actual_Return167_qualification_and_delivery_queue_v3_20261010', 'actual_Return167_priority_candidate_admission_main_v5_20261010', 'actual_recent252_return_own_controls_and_training_queue_v2_20261010', 'actual_recent252_return_qualified_screen_and_main_queue_v3_20261010', 'actual_RecentReturn252_source_and_recovery_admission_main_v6_20261010', 'actual_BF16_medium2048_recent252returnhuber050_seed09_restart_control_v1_20261009', 'actual_BF16_medium2048_recent252returnhuber050_seed09_e64_bank6_v1_20261009', 'actual_RecentReturn252_after167_high_impact65_screen_v1_20261010', 'actual_forward20_own_controls_and_training_queue_v1_20261010', 'actual_forward20_qualified_screen_and_main_queue_v1_20261010', 'actual_Return_after163_high_impact65_screen_v1_20261010', 'actual_Return_after163_65_completion_main_v17_20261010', 'actual_forward20_own_source_admission_main_v3_20261010', 'actual_BF16_medium2048_forward20huber050_seed09_restart_control_v1_20261009', 'BF16Forward20Huber050167_independent_small_CPU_v1_20261009', 'actual_BF16_medium2048_forward20huber050_seed09_e64_bank6_v1_20261009', 'BF16Forward20Huber050167_independent_full5_GPU_controls_v1_20261009', 'BF16Forward20Huber050167_actual_native42_calendar_v1_20261009', 'actual_Forward20_after163_high_impact65_screen_v1_20261010', 'actual_Forward20_after163_65_completion_main_v18_20261010', 'actual_RecentReturn252_after167_65_completion_main_v19_20261010', 'actual_Forward20_after167_high_impact65_screen_v1_20261010', 'actual_Forward20_after167_65_completion_main_v20_20261010', 'actual_shared_string_pack_full167_benchmark_v1_20261010', 'RecentReturn252_after167_selected_native14_v1_20261010', 'RecentReturn252Protected168_complete67_family_v1_20261010', 'RecentReturn252Protected168_selected_candidate_preparation_v1_20261010', 'RecentReturn252Protected168_selected_candidate_sealing_v1_20261010', 'RecentReturn252Protected168_round168_full_registration_v1_20261010', 'actual_recent252_forward20_own_controls_and_training_queue_v1_20261010', 'actual_round168_and_recent252_mean20_preparation_main_v8_20261010', 'actual_BF16_medium2048_recent252forward20huber050_seed09_restart_control_v1_20261009', 'BF16Recent252Forward20Huber050170_independent_small_CPU_v1_20261009', 'actual_BF16_medium2048_recent252forward20huber050_seed09_e64_bank6_v1_20261009', 'BF16Recent252Forward20Huber050170_independent_full5_GPU_controls_v1_20261009', 'BF16Recent252Forward20Huber050170_actual_native42_calendar_v1_20261009']:
            p = A / 'service_owned_workflows_20261006' / name
            row = {'status': 'not_started'}
            if (p / 'native_launch.json').exists():
                l = read(p / 'native_launch.json')
                row = {'status': 'running' if owned(l) else 'closed', 'worker_pid': l['owned_worker_pid']}
                if (p / 'service_execution.json').exists():
                    row['execution'] = read(p / 'service_execution.json')
                    row['status'] = row['execution']['status']
            jobs[name] = row
        bank = Path('E:/赛题五_本机临时/neural_BF16_medium2048_forward20huber050_seed09_e64_bank6_v1_20261009')
        state = {'at_local': now.isoformat(), 'deadline_local': c['stop_at_local'], 'best_fully_qualified': read(A / 'latest_verified_submission_delivery_v2_20261008.json'), 'round166': read(A / 'continuous_fast_reused_frontiers_v22_20261010/state.json'), 'services': jobs, 'forward20_completed_models': [y for y in range(2020, 2026) if (bank / str(y) / 'info.json').exists()], 'forward20_six_fit_verification_complete': (bank / 'verification.json').exists(), 'resources': {'RAM_available_GiB': psutil.virtual_memory().available / 2 ** 30, 'D_free_GiB': shutil.disk_usage('D:/').free / 2 ** 30, 'E_free_GiB': shutil.disk_usage('E:/').free / 2 ** 30}}
        for label, p in [('mean5_65',Path('E:/赛题五_本机临时/Recent252Forward5_after168_high_impact65_screen_v1_20261010')),('rank5_65',Path('E:/赛题五_本机临时/Recent252Rank5_after168_high_impact65_screen_v1_20261010')),('fine31',Path('E:/赛题五_本机临时/RecentReturn252_after167_protected_fine31_screen_v1_20261010')),('joint65',Path('E:/赛题五_本机临时/Recent252Forward20_after168_high_impact65_screen_v1_20261010')),('forward20_training', bank), ('Return65', Path('E:/赛题五_本机临时/Return_after163_high_impact65_screen_v1_20261010')), ('Forward20_65', Path('E:/赛题五_本机临时/Forward20_after163_high_impact65_screen_v1_20261010')), ('Forward20_after167_65', Path('E:/赛题五_本机临时/Forward20_after167_high_impact65_screen_v1_20261010')), ('Recent252_after167_65', Path('E:/赛题五_本机临时/RecentReturn252_after167_high_impact65_screen_v1_20261010'))]:
            state[label] = {k: read(p / file) for k, file in [('stage', 'actual_stage.json'), ('best', 'best_so_far.json')] if (p / file).exists()}
        p = A / 'Return167_qualification_and_delivery_queue_v3_20261010/state.json'
        if p.exists():
            state['Return167'] = read(p)
        p = A / 'github_validation_sync_main_20261005/round167_receipt.json'
        full = A / 'optimization_20261003_r167/full_registration_execution.json'
        completed_round_receipts=[]
        for receipt in (A/'github_validation_sync_main_20261005').glob('round*_receipt.json'):
            r=read(receipt);n=r.get('round');f=A/f'optimization_20261003_r{n}/full_registration_execution.json'
            if n and r.get('status')=='pushed_and_remote_head_verified' and r.get('connected_records') and f.exists() and read(f).get('status')=='passed':completed_round_receipts.append(r)
        board=max(completed_round_receipts,key=lambda r:r['round'])['connected_records']
        latest_round=max(r['round'] for r in completed_round_receipts)
        state['latest_full_registered_round']=latest_round
        combined=Path('E:/赛题五_本机临时/neural_BF16_medium2048_recent252forward20huber050_seed09_e64_bank6_v1_20261009')
        state['recent252_mean20_completed_models']=[y for y in range(2020,2026) if (combined/str(y)/'info.json').exists()]
        five=Path('E:/赛题五_本机临时/neural_BF16_medium2048_recent252forward5huber050_seed09_e64_bank6_v1_20261009')
        state['recent252_mean5_completed_models']=[y for y in range(2020,2026) if (five/str(y)/'info.json').exists()]
        state['mean5_training_stage']=read(five/'actual_stage.json') if (five/'actual_stage.json').exists() else {}
        rankfive=Path('E:/赛题五_本机临时/neural_BF16_medium2048_recent252rank5huber050_seed09_e64_bank6_v1_20261009')
        state['recent252_rank5_completed_models']=[y for y in range(2020,2026) if (rankfive/str(y)/'info.json').exists()]
        state['rank5_training_stage']=read(rankfive/'actual_stage.json') if (rankfive/'actual_stage.json').exists() else {}
        state['actual_complete_round_board_records'] = board
        recent = Path('E:/赛题五_本机临时/neural_BF16_medium2048_recent252returnhuber050_seed09_e64_bank6_v1_20261009')
        state['recent252_completed_models'] = [y for y in range(2020, 2026) if (recent / str(y) / 'info.json').exists()]
        p = A / 'recent252_return_own_controls_and_training_queue_v2_20261010/state.json'
        if p.exists():
            state['recent252_queue'] = read(p)
        rows = []
        for family in ['Recent252Forward5_after168_high_impact65_screen_v1_20261010','Recent252Rank5_after168_high_impact65_screen_v1_20261010','RecentReturn252_after167_protected_fine31_screen_v1_20261010','Recent252Forward20_after168_high_impact65_screen_v1_20261010','high_impact_cumulative_screen_v2_20261010', 'protected_upper_tail_screen_v1_20261010', 'protected_official_top_screen_v2_20261010', 'Huber010_high_impact65_screen_v1_20261010', 'protected_quantization37_screen_v1_20261010', 'budgeted_neural_Top37_screen_v1_20261010', 'causal_neural_smoothing73_screen_v1_20261010', 'TopWeighted_after163_high_impact65_screen_v1_20261010', 'stock_identity_prior_after163_screen33_v4_20261010', 'Return_after163_high_impact65_screen_v1_20261010', 'Forward20_after163_high_impact65_screen_v1_20261010', 'RecentReturn252_after167_high_impact65_screen_v1_20261010', 'Forward20_after167_high_impact65_screen_v1_20261010']:
            for p in (Path('E:/赛题五_本机临时') / family).glob('case*_official.json'):
                r = read(p)
                rows.append({'family': family, 'case': r['case'], 'S': r['connected_final_score'], 'gain': r['score_gain_over_qualified_parent'], 'configuration': r['configuration'], 'source': str(p), 'submission_qualified': False})
        rows.sort(key=lambda r: (-r['S'], r['family'], r['case']))
        state['supplementary_actual_scored_records'] = len(rows)
        write(A / 'high_impact_additional_validation_rankings_v3_20261010.json', {'at_local': now.isoformat(), 'records': rows, 'scores_from_actual_training_only_official_capsules': True, 'complete_round_board_records': board})
        write(A / 'optimization_live_progress_v32_20261010.json', state)
        best = state['best_fully_qualified']
        write(A / 'actual_optimization_fast_runtime_handoff_v36_20261010.json', state)
        p = A / 'optimization_live_progress_v32_20261010.md'
        t = p.with_suffix('.tmp')
        return167 = state.get('Return167', {'status': 'waiting_actual167_qualification_queue'})
        recentbest=state.get('Recent252_after167_65',{}).get('best',{})
        meanbest=state.get('Forward20_after167_65',{}).get('best',{})
        mean5score=state.get('mean5_65',{}).get('best',{});rank5score=state.get('rank5_65',{}).get('best',{})
        fine=state.get('fine31',{}).get('best',{});joint=state.get('joint65',{}).get('best',{})
        text=f"更新时间：{now.isoformat()}\n\n截止：{c['stop_at_local']}\n\n已完全验证最佳：第{best['selected_round']}轮，S={best['official_score']:.12f}；完整榜{board}条（最新完整登记{latest_round}轮）。\n\n近期252日：{recentbest.get('completed_cases',0)}/65，最佳候选S={recentbest.get('best',{}).get('connected_final_score')}，候选完整资格以JSON为准。\n\n20日收益加入完整167：{meanbest.get('completed_cases',0)}/65，最佳候选S={meanbest.get('best',{}).get('connected_final_score')}。\n\n局部细调：{fine.get('completed_cases',0)}/31，S={fine.get('best',{}).get('connected_final_score')}。\n\n联合方案：{joint.get('completed_cases',0)}/65，S={joint.get('best',{}).get('connected_final_score')}。\n\n新5日收益评分：{mean5score.get('completed_cases',0)}/65，S={mean5score.get('best',{}).get('connected_final_score')}。\n\n新5日排名评分：{rank5score.get('completed_cases',0)}/65，S={rank5score.get('best',{}).get('connected_final_score')}。\n\n新5日排名目标训练：{len(state['recent252_rank5_completed_models'])}/6，阶段{state['rank5_training_stage'].get('year','准备中')}。\n\n新5日目标训练：{len(state['recent252_mean5_completed_models'])}/6，阶段{state['mean5_training_stage'].get('year','准备中')}。\n\n新近期252日+20日目标训练：{len(state['recent252_mean20_completed_models'])}/6。\n\n第169轮完整228项登记队列：{jobs['FastNeuralFrontier169_complete228_family_v2_20261010']['status']}；须待全部评分与选中原生检查通过。\n\n资源：D空闲{state['resources']['D_free_GiB']:.2f}GiB，E空闲{state['resources']['E_free_GiB']:.2f}GiB。\n\n详细任务：[进度JSON](optimization_live_progress_v32_20261010.json)\n"
        t.write_text(text,encoding='utf8');t.replace(p)
        if now >= datetime.fromisoformat(c['stop_at_local']) or c['status'] != 'optimization_active_after_explicit_manual_resume':
            return
        time.sleep(20)
if __name__ == '__main__':
    main()
