from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
source=A/'monitor_verified_current_optimization_v149_20261011.py';s=source.read_text(encoding='utf8')
assert s.count(' while True:\n')==1
s=s.replace(' while True:\n'," aliases.update(read(A/'actual_ancestor_guard83_future_scope_admission_v1_20261011.json')['service_alias_updates'])\n names += ['recovery83_StockRank10Embedding192_complete48_family_v1_20261011','actual_original_remaining45_after_recovery83_v84_20261011','actual_rank120_rank60_after183_disagreement_CDFfine8_screen77_v1_20261011','actual_rank120_rank60_after183_consensus8_screen80_v1_20261011','actual_rank120_rank60_after183_consensusWeight8_screen84_v1_20261011','actual_consensusWeight8_results_selection_main85_v1_20261011','actual83_guard85_weights_and_completed_cleanup_sources86_main_v1_20261011']\n while True:\n")
needle="  state['pending_cached_highest_S']=max([.4514130257498636,*score_values(science)])";assert s.count(needle)==1
s=s.replace(needle,"""  for tag,folder in [('CDFfine8','StockRank120Rank60_after183_disagreement_CDFfine8_screen77_v1_20261011'),('consensus8','StockRank120Rank60_after183_consensus8_screen80_v1_20261011'),('new_consensusWeight8','StockRank120Rank60_after183_consensusWeight8_screen84_v1_20261011')]:
   d=Path('E:/赛题五_本机临时')/folder;rs=[read(p) for p in d.glob('case*_official.json')];science[tag]={'completed':len(rs),'expected':8,'best_S':max((r['connected_final_score'] for r in rs),default=None),'actual_full_scoring_complete':(d/'verification.json').exists(),'candidate_qualification_separate':True}
"""+needle)
for old,new in [('progress_v149','progress_v150'),('handoff_v308','handoff_v311'),("+'.149.tmp'","+'.150.tmp'")]:s=s.replace(old,new)
p=A/'monitor_verified_current_optimization_v150_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
name='actual_fast_optimization_progress_reboot_v150_20261011';r=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r)
for _ in range(30):
 if (A/'optimization_live_progress_v150_20261011.json').exists():break
 time.sleep(.2)
assert (A/'optimization_live_progress_v150_20261011.json').exists()
old=A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v149_20261011/native_launch.json';identity=read(old)
if owned(identity):
 import handoff_joint_goss_round97_full_execution_20261006 as h
 parent,worker=h.pair(identity);before=h.stack(worker.pid)
 assert '(idle)' in before and 'main (monitor_verified_current_optimization_v149_20261011.py:' in before and not worker.children(),before
 worker.suspend();parent.suspend();after=h.stack(worker.pid)
 if not ('(idle)' in after and 'main (monitor_verified_current_optimization_v149_20261011.py:' in after and not worker.children()):parent.resume();worker.resume();raise AssertionError(after)
 create(A/'actual_observer149_idle_retired_after150_current_snapshot_v1_20261011.json',{'status':'actual_idle_observer_only_replaced_scientific_workers_preserved','identity':identity,'before':before,'after':after,'snapshot_sha256':sha(A/'optimization_live_progress_v150_20261011.json')});worker.terminate();parent.terminate()
original=A/'build_complete191_plus_completed_raw_TRAIN_score_catalog_v3_20261011.py';s=original.read_text(encoding='utf8').replace('榜_v3_20261011','榜_v4_20261011').replace('location_v3_20261011','location_v4_20261011')
s=s.replace(" assert allowed();closed('actual191_original_QA102_main_delivery_completion_bridge71_v1_20261011')"," assert allowed();closed('actual_consensusWeight8_results_selection_main85_v1_20261011');closed('actual191_original_QA102_main_delivery_completion_bridge71_v1_20261011')")
b=A/'build_complete191_plus_completed_raw_TRAIN_score_catalog_v4_20261011.py';ast.parse(s);assert not b.exists();b.write_text(s,encoding='utf8')
pub=A/'publish_actual_complete191_and_raw_TRAIN_score_catalog_v4_main_v1_20261011.py';s=(A/'publish_actual_complete191_and_raw_TRAIN_score_catalog_v3_main_v1_20261011.py').read_text(encoding='utf8').replace('catalog_v3','catalog_v4').replace('location_v3','location_v4');ast.parse(s);assert not pub.exists();pub.write_text(s,encoding='utf8')
for name,p in [('actual_complete191_plus_completed_raw_TRAIN_score_catalog_v4_20261011',b),('actual_complete191_and_raw_TRAIN_score_catalog_v4_main_v1_20261011',pub)]:
 assert allowed();r=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r)
