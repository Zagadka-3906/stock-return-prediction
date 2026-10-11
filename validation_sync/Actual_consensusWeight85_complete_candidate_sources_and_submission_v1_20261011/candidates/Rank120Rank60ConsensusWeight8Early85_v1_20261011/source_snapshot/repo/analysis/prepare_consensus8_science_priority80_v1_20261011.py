"""Extend the proven pointwise confidence penalty, preserving the official Top protection."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
originalmix=A/'rank120_rank60_disagreement_raw_signal_v1_20261011.py';mixsource=originalmix.read_text(encoding='utf8').replace('(-.5,-.25,0.,.25,.5)','(.5,.75,1.,2.)')
mixpath=A/'rank120_rank60_consensus_raw_signal80_v1_20261011.py';ast.parse(mixsource);assert not mixpath.exists();mixpath.write_text(mixsource,encoding='utf8')
import numpy as np,importlib
mixing=importlib.import_module(mixpath.stem);rng=np.random.default_rng(2026101180);a=rng.normal(size=2000);b=rng.normal(size=2000);a[:4]=[0.,-0.,-1e6,1e6];b[:4]=[-0.,0.,-1e6,-1e6];rows=[]
for k in (.5,.75,1.,2.):
 full=mixing.combine(a,b,k);assert np.array_equal(full.view('u8'),mixing.scalar_oracle(a,b,k).view('u8'))
 for count in (1,100,1700):assert np.array_equal(full[:count].view('u8'),mixing.combine(a[:count],b[:count],k).view('u8'))
 poisoned=b.copy();poisoned[1700:]*=999.;assert np.array_equal(full[:1700].view('u8'),mixing.combine(a,poisoned,k)[:1700].view('u8'))
 rows.append({'penalty':k,'actual_scalar_full_bits_exact':True,'prefix_rows':[1,100,1700],'future_suffix_poison_prior_bits_unchanged':True})
refused=[]
for aa,bb,k in [(a,b,0.),(a[:-1],b,.5),(np.array([np.nan]),np.array([0.]),.75),(a.reshape(2,1000),b.reshape(2,1000),1.)]:
 try:mixing.combine(aa,bb,k)
 except AssertionError:refused.append(True)
 else:raise AssertionError('bad consensus input accepted')
cpu=A/'actual_consensus8_pointwise_CPU_controls80_v1_20261011.json';create(cpu,{'status':'passed_actual4_full_scalar12_prefix4_suffix4_bad_input_refusals','records':rows,'bad_inputs_refused':len(refused),'input_sha256':{str(p):sha(p) for p in [Path(__file__),originalmix,mixpath]},'native_or_TRAIN_scores_not_claimed':True})
original=A/'run_rank120_rank60_after183_disagreement10_screen_v1_20261011.py';s=original.read_text(encoding='utf8');tree=ast.parse(s);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='cases');cases=ast.literal_eval(node.body[0].value)[:2];cases[1]['disagreement_penalty']=.5
cases += [{'kind':'valid_pool_protection_v1','role':'nonflag_valid','weight':w,'sign':1.,'protect_fraction':.2,'disagreement_penalty':k} for k in (.75,1.,2.) for w in (.032,.064)]
lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['def cases():\n    return '+repr(cases)+'\n'];s=''.join(lines)
s=s.replace('StockRank120Rank60_after183_disagreement10_screen_v1','StockRank120Rank60_after183_consensus8_screen80_v1').replace('rank120_rank60_disagreement_raw_signal_v1_20261011','rank120_rank60_consensus_raw_signal80_v1_20261011').replace('rank120_rank60_disagreement_actual_CPU_controls_v1_20261011.json','actual_consensus8_pointwise_CPU_controls80_v1_20261011.json').replace('rank120_rank60_disagreement10_predeclared_sources_admission_v1','rank120_rank60_consensus8_predeclared_sources80_v1')
s=s.replace("    closed('actual_fraction38_completed_namespace_bridge_v1_20261011')","    closed('actual_rank120_rank60_after183_disagreement_CDFfine8_screen77_v1_20261011')\n    closed('actual_completed_disagreement10_pointer_namespace_bridge72_v1_20261011')\n    closed('actual_fraction38_completed_namespace_bridge_v1_20261011')",1)
old="reference=read(Path('E:/赛题五_本机临时/StockRank120Rank60_after183_best_blend_fraction38_screen_v1_20261011/verification.json'))['best']";assert s.count(old)==1;s=s.replace(old,"reference=read(Path('E:/赛题五_本机临时/StockRank120Rank60_after183_disagreement10_screen_v1_20261011/verification.json'))['best']")
for before,after in [("'expected_cases':10","'expected_cases':8"),("'new_quality_score_records':10","'new_quality_score_records':8"),("'actual_nonidentity_full_controls':9","'actual_nonidentity_full_controls':7"),("'actual_nonidentity_prefix_controls':27","'actual_nonidentity_prefix_controls':21"),('passed10_disagreement','passed8_consensus80'),('frozen10_disagreement','frozen8_consensus80'),("A/'actual_StockRank120Rank60_after183_best_blend_fraction38_screen_location_v1_20261011.json'","A/'actual_StockRank120Rank60_after183_consensus8_screen80_location_v1_20261011.json'")]:s=s.replace(before,after)
driver=A/'run_rank120_rank60_after183_consensus8_screen80_v1_20261011.py';ast.parse(s);assert not driver.exists();driver.write_text(s,encoding='utf8')
proof=A/'rank120_rank60_consensus8_predeclared_sources80_v1_20261011.json';create(proof,{'status':'frozen6_uncovered_stronger_horizon_consensus_penalties_before_actual_full_TRAIN_controls_scores_old_best10_reference_bits_required','cases':cases,'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,driver,mixpath,cpu]},'new_fits':0,'actual_future_X_read':False,'test_labels_read':False})
originalqueue=A/'run_actual191_disagreement10_CDF8_and_fine8_priority77_then_original48_v1_20261011.py';queue=originalqueue.read_text(encoding='utf8');needle=" proof=A/'actual_current_completed_parents71_child_propagation_admission_v1_20261011.json'";assert queue.count(needle)==1
queue=queue.replace(needle," closed('actual_consensus8_results_selection_main81_v1_20261011')\n"+needle)
qfile=A/'run_original191_then_all_current_science_priority80_then_original48_v1_20261011.py';ast.parse(queue);assert not qfile.exists();qfile.write_text(queue,encoding='utf8')
folder=A/'service_owned_workflows_20261006/actual191_disagreement10_CDF8_and_fine8_priority77_then_original48_v1_20261011';identity=read(folder/'native_launch.json');assert owned(identity)
import handoff_joint_goss_round97_full_execution_20261006 as h
parent,worker=h.pair(identity);before=h.stack(worker.pid)
def idle(stack):return '(idle)' in stack and ('closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:' in stack or 'main (run_actual191_disagreement10_CDF8_and_fine8_priority77_then_original48_v1_20261011.py:' in stack)
assert idle(before) and not worker.children(),before
worker.suspend();parent.suspend();after=h.stack(worker.pid)
if not (idle(after) and not worker.children()):parent.resume();worker.resume();raise AssertionError(after)
create(A/'actual_idle_priority77_retirement_for_consensus_science80_v1_20261011.json',{'status':'actual_idle_administrative_only_original48_tasks_unchanged_scientific_workers_preserved','identity':identity,'before':before,'after':after});worker.terminate();parent.terminate()
for name,p in [('actual_rank120_rank60_after183_consensus8_screen80_v1_20261011',driver),('actual_original191_then_all_current_science_priority80_then_original48_v1_20261011',qfile)]:
 assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
print({'uncovered_stronger_consensus_cases':6,'actual_CPU_scalar4_prefix12_suffix4_bad4_passed':True,'current_full37_inference_unchanged':True},flush=True)
