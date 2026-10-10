from pathlib import Path
import sys,re,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
old=A/'monitor_actual_chronological_optimization_progress_v53_20261009.py';new=A/'monitor_actual_chronological_optimization_progress_v54_20261009.py'
mapping={
 'optimization_live_progress_v53_20261009':'optimization_live_progress_v54_20261009',
 'PureRFFHuber149_complete_chronological_dispatch_v11_20261009':'PureRFFHuber149_complete_chronological_dispatch_publication_v15_20261009',
 'HuberSparse150_complete_chronological_dispatch_v3_20261009':'HuberSparse150_complete_chronological_dispatch_publication_v16_20261009',
 'RFFSparse151_complete_chronological_dispatch_v2_20261009':'RFFSparse151_complete_chronological_dispatch_publication_v16_20261009',
 'actual149_all5_and152_historical_main_publication_v55_20261009':'actual149_all5_and152_historical_main_publication_v56_20261009'}
s=old.read_text(encoding='utf8');pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)));s=pattern.sub(lambda m:mapping[m[0]],s)
needle="    write(A/'optimization_live_progress_v54_20261009.json',"
assert needle in s
addition="""    frontier=state['sparse_after148_152_frontier']
    frontier.update(complete_quality_receivers_and_prior_duplicate_audit_still_required=status('SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009')['status']!='passed',
        complete_prospective_controls=status('SparseAfter148152_complete_prospective_controls_v1_20261009'),
        duplicate_audit=status('SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009'),
        chronological_dispatch=status('SparseAfter148152_complete_chronological_dispatch_publication_v16_20261009'),
        source_admission=status('SparseAfter14829_round152_source_admission_v1_20261009'),
        official_scoring=status('SparseAfter14829_official_comparison_v1_20261009'),
        prospective_source_routes=32,prospective_graph_controls=200,actual_future_X_read=False)
    q=A/'SparseAfter14829_official_comparison_v1_20261009'
    if (q/'verification.json').exists():frontier['actual_official_scores']=len(read(q/'verification.json')['records'])
    elif (q/'actual_stage.json').exists():frontier['actual_official_scores']=read(q/'actual_stage.json').get('actual_completed_cases',0)
    state['verified_publication_only_large_report_and_research_index_guards']=str(A/'lossless_chunked_safe_main_runtime_v1_20261009.json')
"""
s=s.replace(needle,addition+needle)
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('actual_chronological_optimization_progress_observer_v54_20261009',new.name,[],{str(new):sha(new)})
create(A/'actual_safe_pipeline_progress_hidden_launch_v54_20261009.json',row)
for _ in range(60):
 if (A/'optimization_live_progress_v54_20261009.json').is_file():break
 time.sleep(1)
else:raise AssertionError('New observer did not write its first complete snapshot')
assert owned(row)
create(A/'latest_actual_optimization_progress_pointer_v54_20261009.json',{'status':'actual_current_progress','json':str(A/'optimization_live_progress_v54_20261009.json'),'markdown':str(A/'optimization_live_progress_v54_20261009.md'),'actual_observer':row})
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended,stack
for version in (52,53):
 oldrow=read(A/'service_owned_workflows_20261006'/f'actual_chronological_optimization_progress_observer_v{version}_20261009'/'native_launch.json')
 if owned(oldrow):
  dump=stack(oldrow['owned_worker_pid']);line=next(line for line in dump.splitlines() if '    main (' in line)
  parent,worker,idle=suspended_idle(oldrow,line)
  try:retire_suspended(oldrow,row)
  except BaseException:
   if parent.is_running():parent.resume()
   if worker.is_running():worker.resume()
   raise
print(row['owned_worker_pid'],flush=True)
