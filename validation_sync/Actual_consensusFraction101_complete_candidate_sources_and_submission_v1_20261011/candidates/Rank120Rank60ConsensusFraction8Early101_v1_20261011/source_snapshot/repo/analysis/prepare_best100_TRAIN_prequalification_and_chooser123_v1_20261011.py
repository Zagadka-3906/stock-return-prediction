from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed();closed('actual_rank120_rank60_after183_consensusFraction8_screen100_v1_20261011');closed('actual_rank120_rank60_after183_consensusFractionWeight8_screen108_v1_20261011')
base=Path('E:/赛题五_本机临时');files=[base/'StockRank120Rank60_after183_consensusFraction8_screen100_v1_20261011/verification.json',base/'StockRank120Rank60_after183_consensusFractionWeight8_screen108_v1_20261011/verification.json'];proofs=[read(p) for p in files]
for p in proofs:
 assert len(p['records'])==p['new_quality_score_records']==8 and (p['actual_nonidentity_full_controls'],p['actual_nonidentity_prefix_controls'])==(7,21)
 for file,d in p['input_sha256'].items():assert sha(file)==d,file
 for r in p['records']:
  cap=Path(r['official_score_cache']['official_metrics_source']);assert sha(cap)==r['official_metric_capsule_sha256'] and read(cap)['metrics']==r['metrics']
assert proofs[0]['best']['connected_final_score']>proofs[1]['best']['connected_final_score']
import handoff_joint_goss_round97_full_execution_20261006 as h
identity=read(A/'service_owned_workflows_20261006/actual_final_fraction100_or108_best_only_full_pipeline110_v1_20261011/native_launch.json');assert owned(identity);parent,worker=h.pair(identity);before=h.stack(worker.pid)
def idle(stack):return '(idle)' in stack and 'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:' in stack and 'run_final_score_best_only_fraction100_or108_pipeline110_v1_20261011.py:' in stack
assert idle(before) and not worker.children(),before
worker.suspend();parent.suspend();after=h.stack(worker.pid)
if not (idle(after) and not worker.children()):parent.resume();worker.resume();raise AssertionError(after)
protocol=A/'rank120_rank60_consensusFraction8_early101_sources_admission_v2_20261011.json';wrapper=A/'run_best_only_chooser_with_exact_prequalified101_reuse123_v1_20261011.py';admission=A/'actual_idle_best_only110_replaced_for_TRAIN_native_prequalification123_v1_20261011.json';create(admission,{'status':'actual_idle_administrative_publication_wait_only_replaced_same_verified_best100_one_full_candidate_TRAIN_native14_prequalified_while_weight85_main_verifies','identity':identity,'before':before,'after':after,'actual16_TRAIN_scores':[{str(p):sha(p)} for p in files],'best100_S':proofs[0]['best']['connected_final_score'],'best108_S':proofs[1]['best']['connected_final_score'],'input_sha256':{str(p):sha(p) for p in [Path(__file__),wrapper,protocol]},'actual_future_X_read_by_prequalification':False,'scientific_workers_stopped':0,'test_labels_read':False});worker.terminate();parent.terminate()
for name,driver in [('actual_rank120_rank60_consensusFraction8_early101_normalization_v1_20261011','normalize_rank120_rank60_consensusFraction8_early101_v1_20261011.py'),('actual_rank120_rank60_consensusFraction8_early101_selected_native14_v1_20261011','qualify_rank120_rank60_consensusFraction8_early101_selected_native14_v2_20261011.py')]:
 assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(protocol):sha(protocol)});create(A/(name+'_early123_activation.json'),r)
 if 'normalization' in name:closed(name)
name='actual_best100_only_full_pipeline_prequalified_reuse123_v1_20261011';assert allowed();r=start_service(name,wrapper.name,[],{str(wrapper):sha(wrapper),str(admission):sha(admission)});create(A/(name+'_activation.json'),r)
