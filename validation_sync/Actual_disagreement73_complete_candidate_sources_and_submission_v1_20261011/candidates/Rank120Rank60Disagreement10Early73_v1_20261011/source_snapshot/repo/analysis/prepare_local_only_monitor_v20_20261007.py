"""Observe real119v6 and120v4 closures after actual generator-source recovery."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    actual=read(A/'quantile119_nonflag120_closed_dependency_recovery_actual_launches_v6_20261007.json')['launches']
    mapping={}
    for name in actual:
        if name.startswith('quantile_HGB88'):mapping[name.removesuffix('_v6')+'_v5']=name
        elif name.startswith('nonflag_HGB40'):mapping[name.removesuffix('_v4')+'_v3']=name
    mapping.update({'quantile_HGB88_official_comparison_v5_20261007':'quantile_HGB88_official_comparison_v6_20261007',
      'nonflag_HGB40_official_comparison_v3_20261007':'nonflag_HGB40_official_comparison_v4_20261007',
      'local_only_v19':'local_only_v20','single_host_optimization_live_status_v19_20261007':'single_host_optimization_live_status_v20_20261007'})
    old=A/'monitor_local_only_runtime_v19_20261007.py';text=substitute(old.read_text(encoding='utf8'),mapping)
    target=A/'monitor_local_only_runtime_v20_20261007.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8')
    old_h=A/'handoff_local_only_monitor_v19_20261007.py'
    h=substitute(old_h.read_text(encoding='utf8'),{
      'local_only_monitor_v19_actual_handoff_20261007':'local_only_monitor_v20_actual_handoff_20261007',
      'local_only_progress_monitor_v18':'local_only_progress_monitor_v19','local_only_progress_monitor_v19':'local_only_progress_monitor_v20',
      'monitor_local_only_runtime_v18_20261007.py':'monitor_local_only_runtime_v19_20261007.py','monitor_local_only_runtime_v19_20261007.py':'monitor_local_only_runtime_v20_20261007.py',
      'local_only_v19':'local_only_v20','administrative_supersession_local_v19_20261007':'administrative_supersession_local_v20_20261007',
      'passed_actual_idle_observer18_correct120v3_archive_proof_and_original_science_preserved':'passed_actual_idle_observer19_correct119v6_120v4_closures_and_original_science_preserved'})
    target_h=A/'handoff_local_only_monitor_v20_20261007.py';assert not target_h.exists();compile(h,str(target_h),'exec');target_h.write_text(h,encoding='utf8')
    create(A/'local_only_monitor_v20_source_preparation_20261007.json',{'status':'compiled_real119v6_and120v4_qualified_only_routes',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,old_h,target_h]},'scientific_workers_stopped':0})

if __name__=='__main__':main()
