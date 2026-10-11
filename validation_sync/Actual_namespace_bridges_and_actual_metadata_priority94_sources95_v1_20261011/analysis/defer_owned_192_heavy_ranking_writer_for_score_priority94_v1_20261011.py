from pathlib import Path
from datetime import datetime
import sys,time,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
import handoff_joint_goss_round97_full_execution_20261006 as h
assert allowed()
name='recovery58_StockRank10Embedding192_round192_full_registration_v1_20261011';folder=A/'service_owned_workflows_20261006'/name;identity=read(folder/'native_launch.json');assert owned(identity) and not (folder/'service_execution.json').exists()
def metadata_writer(stack):
 return 'build_all_model_rankings_20261003.py:' in stack and ('write_exact_report (byte_exact_ranking_stream_runtime_v1_20261010.py:' in stack or 'native_digest (shared_live_ranking_report_runtime_v3_20261011.py:' in stack)
parent,worker=h.pair(identity);before=h.stack(worker.pid);assert metadata_writer(before) and not worker.children(),before
assert worker.memory_info().rss>12*2**30
assert not (A/'optimization_20261003_r192/full_registration_execution.json').exists() and not (A/'github_validation_sync_main_20261005/round192_receipt.json').exists()
scoreproof=A/'stock_rank10_embedding48_after191_normalized_v1_20261011/pilot48.json'
files={str(p):{'size':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns} for p in (A/'optimization_20261003_r192').rglob('*') if p.is_file()}
worker.suspend();parent.suspend();after=h.stack(worker.pid)
if not (metadata_writer(after) and not worker.children()):parent.resume();worker.resume();raise AssertionError(after)
record={'status':'interrupted_owned_metadata_ranking_writer_only_for_explicit_highest_score_deadline_priority_not_scoring_or_training','at_local':datetime.now().isoformat(),'identity':identity,'before':before,'after':after,'rss_bytes':worker.memory_info().rss,'partial_registration_files_preserved':files,'official_score_records_untouched':True,'native_models_and_completed_candidates_untouched':True,'full192_registration_not_complete':True,'future45_scope_preserved_not_dispatched':True,'restart_requires_existing_output_audit_not_blind_rerun':True,'input_sha256':{str(Path(__file__)):sha(__file__),str(folder/'native_launch.json'):sha(folder/'native_launch.json')}}
create(A/'actual_192_heavy_ranking_writer_interruption_for_score_priority94_v1_20261011.json',record);create(folder/'observation_interruption.json',record)
worker.terminate();parent.terminate()
for _ in range(30):
 if not owned(identity):break
 time.sleep(.1)
assert not owned(identity)
create(A/'actual_192_heavy_ranking_writer_memory_release94_v1_20261011.json',{'status':'verified_owned_metadata_writer_stopped_no_completed_registration_claim','at_local':datetime.now().isoformat(),'available_memory_bytes':psutil.virtual_memory().available,'interruption_record_sha256':sha(A/'actual_192_heavy_ranking_writer_interruption_for_score_priority94_v1_20261011.json')})
