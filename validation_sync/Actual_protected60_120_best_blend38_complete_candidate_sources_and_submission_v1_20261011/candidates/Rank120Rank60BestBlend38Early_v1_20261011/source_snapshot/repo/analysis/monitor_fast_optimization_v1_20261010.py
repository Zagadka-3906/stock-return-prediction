"""Lightweight actual status snapshots for the resumed single-host pipeline."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys,time,os
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from scheduled_user_pause_20261007 import write

def main():
    import psutil
    alias=read(A/'manual_resume_service_aliases_v2_20261010.json')['service_aliases']
    while True:
        control=read(A/'current_user_runtime_control_20261010.json')
        current=datetime.now(timezone(timedelta(hours=8)))
        stages={}
        names={**alias,'main_publisher_v10_20261009':'main_publisher_v11_20261010',
               'BF16Drop05_156_complete_chronological_dispatch_v3_20261009':'BF16Drop05_156_complete_chronological_dispatch_manual_resume_v3_20261010'}
        names.update({n:n for n in [
          *['BF16Drop05_81_'+suffix+'_v1_20261009' for suffix in ('round156_source_admission','controls_main_publication','official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing','round156_full_registration')],
          'BF16FlagAfter15222_official_comparison_v3_20261009','BF16FlagAfter15222_round157_full_registration_v1_20261009']})
        for logical,name in names.items():
            folder=A/'service_owned_workflows_20261006'/name
            row={'service':name,'status':'not_started'}
            if (folder/'native_launch.json').is_file():
                launch=read(folder/'native_launch.json')
                row.update(worker_pid=launch['owned_worker_pid'],status='running' if owned(launch) else 'stopped_or_finished')
                if (folder/'service_execution.json').is_file():row['execution']=read(folder/'service_execution.json');row['status']=row['execution']['status']
                log=folder/'stdout.log'
                if log.is_file():
                    with log.open('rb') as stream:
                        stream.seek(max(0,log.stat().st_size-2200));row['recent_log']=stream.read().decode('utf8',errors='replace')[-1300:]
            stages[logical]=row
        bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009')
        state={'status':'actual_optimization_running_until_explicit_deadline',
               'at_local':current.isoformat(),'deadline_local':control['stop_at_local'],
               'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
               'completed_drop05_annual_models':[y for y in range(2020,2026) if (bank/str(y)/'info.json').is_file()],
               'annual_training_stage':read(bank/'actual_stage.json'),'jobs':stages,
               'available_memory_GiB':psutil.virtual_memory().available/2**30,
               'disk_free_GiB':{d:psutil.disk_usage(d+':/').free/2**30 for d in ('D','E')},
               'new_scores_by_observer':0,'test_labels_read':False}
        for number,family in ((156,'BF16Drop05_81'),(157,'BF16FlagAfter15222')):
            folder=A/(family+'_official_comparison_v1_20261009')
            state['round'+str(number)]={'actual_saved_score_records':len(list(folder.glob('case*_official.json'))),
                                     'complete':(folder/'verification.json').is_file()}
            if state['round'+str(number)]['complete']:state['round'+str(number)]['best']=read(folder/'verification.json')['best']
        write(A/'optimization_live_progress_v1_20261010.json',state)
        text=f"更新时间：{state['at_local']}\n\n优化截止：{state['deadline_local']}\n\n当前最佳合格方案：第{state['best_fully_qualified']['selected_round']}轮，官方S={state['best_fully_qualified']['official_score']:.15f}\n\n第156轮年度模型：{len(state['completed_drop05_annual_models'])}/6；官方分数：{state['round156']['actual_saved_score_records']}/81\n\n第157轮官方分数：{state['round157']['actual_saved_score_records']}/22\n\n各任务状态以同名JSON为准。\n"
        target=A/'optimization_live_progress_v1_20261010.md';temporary=target.with_suffix('.tmp')
        temporary.write_text(text,encoding='utf8');os.replace(temporary,target)
        if current>=datetime.fromisoformat(control['stop_at_local']) or control['status']!='optimization_active_after_explicit_manual_resume':break
        time.sleep(20)

if __name__=='__main__':main()
