"""Observe actual120v3 qualification and measured archive controls."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    old=A/'monitor_local_only_runtime_v18_20261007.py';jobs=read(A/'nonflag_HGB40_complete_pipeline_actual_hidden_launches_20261007.json')['launches']
    mapping={n:n+'_v3' for n in jobs}
    mapping.update({'nonflag_HGB40_official_comparison_v2_20261007':'nonflag_HGB40_official_comparison_v3_20261007',
      'local_only_v18':'local_only_v19','single_host_optimization_live_status_v18_20261007':'single_host_optimization_live_status_v19_20261007'})
    text=substitute(old.read_text(encoding='utf8'),mapping)
    needle="    value['no_full_qualification_claim_from_partial_case_counts']=True";assert text.count(needle)==1
    text=text.replace(needle,"""    archive=A/'exact_native_JSON_full_board_benchmark_20261007/verification.json'
    if archive.exists():
        proof=read(archive);value['actual_exact_native_archive_benchmark']={k:v for k,v in proof.items() if k in ('status','median_measured_subset_encoding_and_compression_speedup','actual_whole_board_encoding_and_compression_seconds','full_original_bytes')}
    archive_runtime=A/'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json'
    if archive_runtime.exists():value['actual_full_archive_runtime']=read(archive_runtime)
"""+needle)
    target=A/'monitor_local_only_runtime_v19_20261007.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8')
    old_h=A/'handoff_local_only_monitor_v18_20261007.py'
    h=substitute(old_h.read_text(encoding='utf8'),{
      'local_only_monitor_v18_actual_handoff_20261007':'local_only_monitor_v19_actual_handoff_20261007',
      'local_only_progress_monitor_v17':'local_only_progress_monitor_v18','local_only_progress_monitor_v18':'local_only_progress_monitor_v19',
      'monitor_local_only_runtime_v17_20261007.py':'monitor_local_only_runtime_v18_20261007.py','monitor_local_only_runtime_v18_20261007.py':'monitor_local_only_runtime_v19_20261007.py',
      'local_only_v18':'local_only_v19','administrative_supersession_local_v18_20261007':'administrative_supersession_local_v19_20261007',
      'passed_actual_idle_observer17_correct_v5_and120_qualified_only_routes_science_preserved':'passed_actual_idle_observer18_correct120v3_archive_proof_and_original_science_preserved'})
    target_h=A/'handoff_local_only_monitor_v19_20261007.py';assert not target_h.exists();compile(h,str(target_h),'exec');target_h.write_text(h,encoding='utf8')
    create(A/'local_only_monitor_v19_source_preparation_20261007.json',{'status':'compiled_actual120v3_qualified_only_routes_and_archive_measures',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,old_h,target_h]},'scientific_workers_stopped':0})

if __name__=='__main__':main()
