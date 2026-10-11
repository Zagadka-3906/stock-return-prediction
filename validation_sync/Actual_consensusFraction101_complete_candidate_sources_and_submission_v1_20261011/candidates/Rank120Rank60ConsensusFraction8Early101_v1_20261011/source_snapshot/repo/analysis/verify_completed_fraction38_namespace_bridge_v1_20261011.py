from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
name='actual_stock_rank60_after183_protected_fraction38_screen_v1_20261011'
service=A/'service_owned_workflows_20261006'/name
while not (service/'service_execution.json').exists():assert allowed();time.sleep(5)
terminal=read(service/'service_execution.json');assert terminal['status']=='failed' and 'FileExistsError' in terminal['failure'],terminal
identity=read(service/'native_launch.json');assert not owned(identity)
pointer=A/'actual_StockRank60EmbeddingSmall512_after183_direct_allocation33_screen_location_v1_20261011.json'
original=read(pointer);assert 'direct_allocation33_screen' in original['output'] and read(Path(original['output'])/'verification.json')['new_quality_score_records']==33
out=Path('E:/赛题五_本机临时/StockRank60EmbeddingSmall512_after183_protected_fraction38_screen_v1_20261011');proof=read(out/'verification.json')
assert proof['new_quality_score_records']==len(proof['records'])==38
assert (proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls'])==(37,111)
for p,d in proof['input_sha256'].items():assert sha(p)==d,p
for row in proof['records']:
 c=out/f"case{row['case']:03d}_controls.json";r=out/f"case{row['case']:03d}_official.json";capsule=Path(row['official_score_cache']['official_metrics_source'])
 assert read(r)==row and sha(c)==row['control_sha256'] and sha(capsule)==row['official_metric_capsule_sha256']
 assert read(capsule)['metrics']==row['metrics'] and read(c)['numeric_sha256']==row['prediction_numeric_sha256']
 if row['case']:assert read(c)['full_independent_Pandas_exact'] and [x['days'] for x in read(c)['prefix_controls']]==[80,260,975]
create(A/'actual_StockRank60EmbeddingSmall512_after183_protected_fraction38_screen_location_v2_20261011.json',{'output':str(out),'verification_sha256':sha(out/'verification.json')})
create(A/'actual_fraction38_completed_only_terminal_namespace_collision_bridge_v1_20261011.json',{'status':'passed_all_actual38_official_capsules_full37_prefix111_original_scores_unchanged_only_final_pointer_namespace_collision','input_sha256':{str(out/'verification.json'):sha(out/'verification.json'),str(service/'service_execution.json'):sha(service/'service_execution.json'),str(pointer):sha(pointer),str(Path(__file__)):sha(__file__)},'actual_original_terminal':terminal,'original33_pointer_preserved':True,'new_fits_or_scores':0,'completed_official_records':38})
print({'verified_completed_actual_records':38,'original_failure_retained':True},flush=True)
