"""Current actual pipelines, compact progress, and complete supplementary score inventory."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from scheduled_user_pause_20261007 import write
def main():
    import psutil
    while True:
        now=datetime.now(timezone(timedelta(hours=8)));c=read(A/'current_user_runtime_control_20261010.json')
        jobs={}
        for name in ['ReturnProtected167_complete67_family_recovery_v3_20261010','ReturnProtected167_selected_native14_v1_20261010','ReturnProtected167_selected_candidate_preparation_v1_20261010','ReturnProtected167_selected_candidate_sealing_v1_20261010','ReturnProtected167_round167_full_registration_v1_20261010','actual_Return167_qualification_and_delivery_queue_v2_20261010','actual_Return167_priority_candidate_admission_main_v5_20261010','actual_recent252_return_own_controls_and_training_queue_v2_20261010','actual_recent252_return_qualified_screen_and_main_queue_v2_20261010','actual_RecentReturn252_source_and_recovery_admission_main_v6_20261010','actual_BF16_medium2048_recent252returnhuber050_seed09_restart_control_v1_20261009','actual_BF16_medium2048_recent252returnhuber050_seed09_e64_bank6_v1_20261009','actual_RecentReturn252_after167_high_impact65_screen_v1_20261010','actual_forward20_own_controls_and_training_queue_v1_20261010','actual_forward20_qualified_screen_and_main_queue_v1_20261010','actual_Return_after163_high_impact65_screen_v1_20261010','actual_Return_after163_65_completion_main_v17_20261010','actual_forward20_own_source_admission_main_v3_20261010','actual_BF16_medium2048_forward20huber050_seed09_restart_control_v1_20261009','BF16Forward20Huber050167_independent_small_CPU_v1_20261009','actual_BF16_medium2048_forward20huber050_seed09_e64_bank6_v1_20261009','BF16Forward20Huber050167_independent_full5_GPU_controls_v1_20261009','BF16Forward20Huber050167_actual_native42_calendar_v1_20261009','actual_Forward20_after163_high_impact65_screen_v1_20261010']:
            p=A/'service_owned_workflows_20261006'/name;row={'status':'not_started'}
            if (p/'native_launch.json').exists():
                l=read(p/'native_launch.json');row={'status':'running' if owned(l) else 'closed','worker_pid':l['owned_worker_pid']}
                if (p/'service_execution.json').exists():row['execution']=read(p/'service_execution.json');row['status']=row['execution']['status']
            jobs[name]=row
        bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_forward20huber050_seed09_e64_bank6_v1_20261009')
        state={'at_local':now.isoformat(),'deadline_local':c['stop_at_local'],'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),'round166':read(A/'continuous_fast_reused_frontiers_v22_20261010/state.json'),'services':jobs,'forward20_completed_models':[y for y in range(2020,2026) if (bank/str(y)/'info.json').exists()],'forward20_six_fit_verification_complete':(bank/'verification.json').exists(),'resources':{'RAM_available_GiB':psutil.virtual_memory().available/2**30,'D_free_GiB':shutil.disk_usage('D:/').free/2**30,'E_free_GiB':shutil.disk_usage('E:/').free/2**30}}
        for label,p in [('forward20_training',bank),('Return65',Path('E:/赛题五_本机临时/Return_after163_high_impact65_screen_v1_20261010')),('Forward20_65',Path('E:/赛题五_本机临时/Forward20_after163_high_impact65_screen_v1_20261010'))]:
            state[label]={k:read(p/file) for k,file in [('stage','actual_stage.json'),('best','best_so_far.json')] if (p/file).exists()}
        p=A/'Return167_qualification_and_delivery_queue_v2_20261010/state.json'
        if p.exists():state['Return167']=read(p)
        p=A/'github_validation_sync_main_20261005/round167_receipt.json'
        full=A/'optimization_20261003_r167/full_registration_execution.json'
        board=read(p)['connected_records'] if p.exists() and full.exists() and read(full)['status']=='passed' else 15852
        state['actual_complete_round_board_records']=board
        recent=Path('E:/赛题五_本机临时/neural_BF16_medium2048_recent252returnhuber050_seed09_e64_bank6_v1_20261009')
        state['recent252_completed_models']=[y for y in range(2020,2026) if (recent/str(y)/'info.json').exists()]
        p=A/'recent252_return_own_controls_and_training_queue_v2_20261010/state.json'
        if p.exists():state['recent252_queue']=read(p)
        rows=[]
        for family in ['high_impact_cumulative_screen_v2_20261010','protected_upper_tail_screen_v1_20261010','protected_official_top_screen_v2_20261010','Huber010_high_impact65_screen_v1_20261010','protected_quantization37_screen_v1_20261010','budgeted_neural_Top37_screen_v1_20261010','causal_neural_smoothing73_screen_v1_20261010','TopWeighted_after163_high_impact65_screen_v1_20261010','stock_identity_prior_after163_screen33_v4_20261010','Return_after163_high_impact65_screen_v1_20261010','Forward20_after163_high_impact65_screen_v1_20261010','RecentReturn252_after167_high_impact65_screen_v1_20261010']:
            for p in (Path('E:/赛题五_本机临时')/family).glob('case*_official.json'):
                r=read(p);rows.append({'family':family,'case':r['case'],'S':r['connected_final_score'],'gain':r['score_gain_over_qualified_parent'],'configuration':r['configuration'],'source':str(p),'submission_qualified':False})
        rows.sort(key=lambda r:(-r['S'],r['family'],r['case']));state['supplementary_actual_scored_records']=len(rows)
        write(A/'high_impact_additional_validation_rankings_v2_20261010.json',{'at_local':now.isoformat(),'records':rows,'scores_from_actual_training_only_official_capsules':True,'complete_round_board_records':board})
        write(A/'optimization_live_progress_v24_20261010.json',state)
        best=state['best_fully_qualified']
        write(A/'actual_optimization_fast_runtime_handoff_v23_20261010.json',state)
        p=A/'optimization_live_progress_v24_20261010.md';t=p.with_suffix('.tmp')
        return167=state.get('Return167',{'status':'waiting_actual167_qualification_queue'})
        t.write_text(f"更新时间：{now.isoformat()}\n\n截止：{c['stop_at_local']}\n\n当前合格最佳：第{best['selected_round']}轮，S={best['official_score']}\n\n完整榜：{board}条；新增独立方案评分：{len(rows)}条（包含重复锚点）。\n\n20日收益目标年度训练：{len(state['forward20_completed_models'])}/6。\n\n直接收益率组合进度：{state['Return65']}\n\n近期252交易日网络：{state.get('recent252_queue',{})}\n\n第167轮候选资格检查：{return167}\n\n任务与资源详情：[进度JSON](optimization_live_progress_v24_20261010.json)\n",encoding='utf8');t.replace(p)
        if now>=datetime.fromisoformat(c['stop_at_local']) or c['status']!='optimization_active_after_explicit_manual_resume':return
        time.sleep(20)
if __name__=='__main__':main()
