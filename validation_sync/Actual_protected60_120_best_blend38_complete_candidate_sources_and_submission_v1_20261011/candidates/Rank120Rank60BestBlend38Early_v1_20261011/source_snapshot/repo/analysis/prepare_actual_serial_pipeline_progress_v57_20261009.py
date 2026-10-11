from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    old=A/'monitor_actual_chronological_optimization_progress_v56_20261009.py';new=A/'monitor_actual_chronological_optimization_progress_v57_20261009.py'
    s=old.read_text(encoding='utf8').replace('optimization_live_progress_v56_20261009','optimization_live_progress_v57_20261009')
    needle="    write(A/'optimization_live_progress_v57_20261009.json',";assert s.count(needle)==1
    addition="""    for number in (150,151):
        prefix='HuberSparse59' if number==150 else 'RFFSparse59';version=3 if number==150 else 2
        row=pipeline[str(number)]
        for field,stem in (('quality','official_comparison'),('scores_main','scores_main_publication'),('selected_candidate','selected_candidate_preparation'),('candidate_sealing','selected_candidate_sealing'),('full_registration',f'round{number}_full_registration')):
            row[field]=status(f'{prefix}_{stem}_v{version}_20261009')
        row['controls_main']=status(f'{prefix}_controls_main_publication_v2_20261009')
        row['failed_original_services_retained']=True
    state['huber_sparse150_frontier'].update(duplicate_audit=status('HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009'),actual_official_scores=pipeline['150']['completed_cases'],serial_recovery=status('HuberSparse59_official_comparison_v3_20261009'))
    state['rff_sparse151_frontier'].update(duplicate_audit=status('RFFSparse151_prior_complete_forecast_duplicate_audit_v3_20261009'),chronological_dispatch=status('RFFSparse151_complete_chronological_dispatch_serial_v22_20261009'))
    state['sparse_after148_152_frontier'].update(duplicate_audit=status('SparseAfter148152_prior_complete_forecast_duplicate_audit_v3_20261009'),chronological_dispatch=status('SparseAfter148152_complete_chronological_dispatch_serial_v22_20261009'),source_admission=status('SparseAfter14829_round152_source_admission_v2_20261009'),official_scoring=status('SparseAfter14829_official_comparison_v2_20261009'))
    state['medium153_frontier'].update(complete_prospective=status('BF16Medium153_complete_prospective_controls_v1_20261009'),prospective_sources=40,prospective_graph_controls=1500,duplicate_audit=status('BF16Medium153_prior_complete_forecast_duplicate_audit_v3_20261009'),chronological_dispatch=status('BF16Medium153_complete_chronological_dispatch_serial_v22_20261009'),source_admission=status('BF16Medium78_round153_source_admission_v1_20261009'),official_scoring=status('BF16Medium78_official_comparison_v1_20261009'),historical_full_controls_main=status('medium153_fulltraining_main_publication_v63_20261009'))
    state['serial_publication_main_lock_actual_two_process_proof']=str(A/'serial_main_publication_mutex_v1_20261009.json')
    q=A/'BF16Medium78_official_comparison_v1_20261009'
    if (q/'verification.json').exists():state['medium153_frontier']['official_scores']=len(read(q/'verification.json')['records'])
    elif (q/'actual_stage.json').exists():state['medium153_frontier']['official_scores']=read(q/'actual_stage.json').get('actual_completed_cases',0)
"""
    s=s.replace(needle,addition+needle)
    compile(s,str(new),'exec')
    with new.open('x',encoding='utf8') as f:f.write(s)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('actual_chronological_optimization_progress_observer_v57_20261009',new.name,[],{str(new):sha(new)})
    create(A/'actual_serial_pipeline_progress_hidden_launch_v57_20261009.json',row)
    for _ in range(30):
        if (A/'optimization_live_progress_v57_20261009.json').exists():break
        time.sleep(1)
    else:raise AssertionError('No first complete snapshot')
    assert owned(row)
    create(A/'latest_actual_optimization_progress_pointer_v57_20261009.json',{'status':'actual_current_progress','json':str(A/'optimization_live_progress_v57_20261009.json'),'markdown':str(A/'optimization_live_progress_v57_20261009.md'),'actual_observer':row})
    from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
    previous=read(A/'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v56_20261009/native_launch.json')
    if owned(previous):
        line=next(line for line in stack(previous['owned_worker_pid']).splitlines() if '    main (' in line)
        parent,worker,idle=suspended_idle(previous,line)
        try:retire_suspended(previous,row)
        except BaseException:
            if parent.is_running():parent.resume()
            if worker.is_running():worker.resume()
            raise
        create(A/'actual_serial_pipeline_progress_handoff_v57_20261009.json',{'old':previous,'new':row,'old_idle_stack':idle,'scientific_jobs_retired':0})
    print(row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
