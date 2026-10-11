from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
source=A/'monitor_verified_current_optimization_v150_20261011.py';s=source.read_text(encoding='utf8')
s=s.replace(" return {'status':t['status'] if t else 'running' if i and owned(i) else 'not_started_or_not_owned','terminal':t,'identity':i}"," interruption=read(d/'observation_interruption.json') if (d/'observation_interruption.json').exists() else None\n return {'status':t['status'] if t else 'interrupted_metadata_only' if interruption and not (i and owned(i)) else 'running' if i and owned(i) else 'not_started_or_not_owned','terminal':t,'identity':i,'interruption':interruption}")
aliases={'actual_rank120_rank60_after183_consensusWeight8_screen84_v1_20261011':'actual_completed_weight84_namespace_bridge90_v1_20261011','actual_consensusWeight8_results_selection_main85_v1_20261011':'actual_completed_weight85_full_pipeline90_v1_20261011','actual_rank120_rank60_after183_consensusFraction8_screen88_v1_20261011':'actual_completed_fraction88_namespace_bridge91_v1_20261011','actual_consensusFraction8_results_selection_main89_v1_20261011':'actual_completed_fraction89_full_pipeline92_v1_20261011'}
assert s.count(' while True:\n')==1;s=s.replace(' while True:\n',' aliases.update('+repr(aliases)+')\n names += '+repr(list(aliases.values())+['actual_completed_weight84_actual8_early96_main_v1_20261011','actual_complete191_plus_completed_raw_TRAIN_score_catalog_v5_20261011','actual_complete191_and_raw_TRAIN_score_catalog_v5_main_v1_20261011'])+'\n while True:\n')
needle="  state['pending_cached_highest_S']=max([.4514130257498636,*score_values(science)])";assert s.count(needle)==1;s=s.replace(needle,"  d=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_consensusFraction8_screen88_v1_20261011');rs=[read(p) for p in d.glob('case*_official.json')];science['new_consensusFraction8']={'completed':len(rs),'expected':8,'best_S':max((r['connected_final_score'] for r in rs),default=None),'actual_full_scoring_complete':(d/'verification.json').exists(),'candidate_qualification_separate':True}\n  state['metadata192_interruption_for_highest_score_priority']=read(A/'actual_192_heavy_ranking_writer_interruption_for_score_priority94_v1_20261011.json')\n"+needle)
for old,new in [('progress_v150','progress_v151'),('handoff_v311','handoff_v312'),("+'.150.tmp'","+'.151.tmp'")]:s=s.replace(old,new)
p=A/'monitor_verified_current_optimization_v151_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');name='actual_fast_optimization_progress_reboot_v151_20261011';r=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r)
for _ in range(30):
 if (A/'optimization_live_progress_v151_20261011.json').exists():break
 time.sleep(.2)
assert (A/'optimization_live_progress_v151_20261011.json').exists()
identity=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v150_20261011/native_launch.json')
if owned(identity):
 import handoff_joint_goss_round97_full_execution_20261006 as h
 parent,worker=h.pair(identity);before=h.stack(worker.pid);assert '(idle)' in before and 'main (monitor_verified_current_optimization_v150_20261011.py:' in before and not worker.children(),before
 worker.suspend();parent.suspend();after=h.stack(worker.pid)
 if not ('(idle)' in after and 'main (monitor_verified_current_optimization_v150_20261011.py:' in after and not worker.children()):parent.resume();worker.resume();raise AssertionError(after)
 create(A/'actual_observer150_idle_retired_after151_namespace_snapshot_v1_20261011.json',{'status':'actual_idle_observer_only_replaced_scientific_workers_preserved','identity':identity,'before':before,'after':after,'snapshot_sha256':sha(A/'optimization_live_progress_v151_20261011.json')});worker.terminate();parent.terminate()
