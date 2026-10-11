from pathlib import Path
import sys,time,math
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
kind=sys.argv[1];assert kind in ('weight84','fraction88')
name='actual_rank120_rank60_after183_'+('consensusWeight8_screen84' if kind=='weight84' else 'consensusFraction8_screen88')+'_v1_20261011';f=A/'service_owned_workflows_20261006'/name
while allowed() and (not (f/'service_execution.json').exists() or owned(read(f/'native_launch.json'))):time.sleep(5)
assert allowed();terminal=read(f/'service_execution.json');assert terminal['status']=='failed' and terminal['failure'].startswith('FileExistsError:') and 'actual_StockRank120Rank60_after183_consensus8_screen80_location_v1_20261011.json' in terminal['failure'],terminal
folder=Path('E:/赛题五_本机临时')/('StockRank120Rank60_after183_'+('consensusWeight8_screen84' if kind=='weight84' else 'consensusFraction8_screen88')+'_v1_20261011');report=read(folder/'verification.json')
assert report['new_quality_score_records']==len(report['records'])==8 and (report['actual_nonidentity_full_controls'],report['actual_nonidentity_prefix_controls'])==(7,21) and report['test_labels_read'] is False
for p,d in report['input_sha256'].items():assert sha(p)==d,p
for i,row in enumerate(report['records']):
 assert row['case']==i and read(folder/f'case{i:03d}_official.json')==row
 cap=Path(row['official_score_cache']['official_metrics_source']);assert sha(cap)==row['official_metric_capsule_sha256'] and read(cap)['metrics']==row['metrics']
 controls=folder/f'case{i:03d}_controls.json';assert sha(controls)==row['control_sha256'];cc=read(controls);assert cc['numeric_sha256']==row['prediction_numeric_sha256'] and cc['rows']==5635800
 if i:assert cc['full_independent_Pandas_exact'] and len(cc['prefix_controls'])==3 and all(x['native_and_independent_bits_exact'] for x in cc['prefix_controls'])
 m=row['metrics'];assert math.isclose(m['final_score'],.4*m['ic_mean']+.3*m['annual_excess']+.3*(1-m['mean_turnover']),abs_tol=1e-12,rel_tol=0)
old=read(Path('E:/赛题五_本机临时/StockRank120Rank60_after183_disagreement10_screen_v1_20261011/verification.json'))['best'];assert report['records'][1]['metrics']==old['metrics'] and report['records'][1]['prediction_numeric_sha256']==old['prediction_numeric_sha256']
pointer=A/('actual_StockRank120Rank60_after183_'+('consensusWeight8_screen84' if kind=='weight84' else 'consensusFraction8_screen88')+'_location_v1_20261011.json');create(pointer,{'output':str(folder),'verification_sha256':sha(folder/'verification.json')})
create(A/('actual_completed_'+kind+'_pointer_namespace_bridge90_v1_20261011.json'),{'status':'passed_actual8_full_TRAIN_all8_official_metrics_7_full21_prefix_controls_completed_only_final_old_pointer_collision_bridged_no_rescoring','input_sha256':{str(p):sha(p) for p in [Path(__file__),folder/'verification.json',f/'service_execution.json',pointer]},'original_failed_terminal_preserved':terminal,'new_scores':0,'test_labels_read':False})
