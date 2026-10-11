from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
service=A/'service_owned_workflows_20261006/actual187_completed_QA_publication_only_resume47_v1_20261011';terminal=read(service/'service_execution.json')
assert terminal['status']=='failed' and 'FileExistsError' in terminal['failure'] and 'original_encoder_binding.json' in terminal['failure'] and not owned(read(service/'native_launch.json'))
release=A/'optimization_20261003_r187';receipt=A/'github_validation_sync_main_20261005/round187_receipt.json';scope=read(release/'provenance_scope_execution.json')
assert read(release/'full_registration_execution.json')['status']=='passed' and scope['status']=='passed'
r=read(receipt);assert r['status']=='pushed_and_remote_head_verified' and (r['round'],r['scored_records'],r['connected_records'],r['actual_full_QA_version'])==(187,88,17490)
for p,d in scope['input_sha256'].items():assert sha(p)==d,p
native=A/'shared_live_ranking_report_round187_execution_v1_20261011.json';assert read(native)['status']=='passed_actual_native_graph_capture_and_private_codec_QA_reader_restored'
assert sha(ROOT/'results/all_model_rankings_20261003.json')==read(native)['native_sha256']
candidate=ROOT/'candidates/optimization_20261003_r187';proof=read(candidate/'verification.json');assert proof['status']=='passed' and (proof['rows'],proof['days'],proof['codes'])==(1599600,344,4650)
for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert proof[key]
assert sha(candidate/'submission.csv')==proof['csv_sha256']
assert read(release/'calibrated_csv_official.json')['metrics']['final_score']==r['official_score']
create(A/'actual187_completed_QA_main_only_finally_log_collision_bridge56_v1_20261011.json',{'status':'passed_actual187_all88_main_QA98_native_bytes_provenance_and_candidate_complete_original_finally_log_FileExists_retained','input_sha256':{str(p):sha(p) for p in [Path(__file__),service/'service_execution.json',service/'stderr.log',receipt,release/'full_registration_execution.json',release/'provenance_scope_execution.json',native,candidate/'verification.json']},'main_receipt':r,'original_terminal':terminal,'new_fits_scores_or_publications':0,'original_failure_preserved':True,'test_labels_read':False})
print({'actual_complete_round':187,'main':r['commit'],'original_log_collision_preserved':True},flush=True)
