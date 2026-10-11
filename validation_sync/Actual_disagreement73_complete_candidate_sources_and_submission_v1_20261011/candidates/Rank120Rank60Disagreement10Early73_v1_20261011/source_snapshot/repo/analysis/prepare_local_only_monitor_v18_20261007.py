"""Observe actual v5 recovery and the admitted-gated nonflag120 pipeline."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    old=A/'monitor_local_only_runtime_v17_20261007.py'
    previous=read(A/'local_118_119_protocol_recovery_actual_hidden_launches_v4_20261007.json')['launches']
    mapping={n:n.removesuffix('_v4')+'_v5' for n in previous}
    for stem in ['HGB_quarter_numeric28','quantile_HGB88']:
        mapping[stem+'_official_comparison_v4_20261007']=stem+'_official_comparison_v5_20261007'
    mapping.update({'local_only_v17':'local_only_v18','single_host_optimization_live_status_v17_20261007':'single_host_optimization_live_status_v18_20261007'})
    text=substitute(old.read_text(encoding='utf8'),mapping)
    needle="'nonflag_HGB10_actual_controls_main_publication')"
    assert text.count(needle)==1
    services=read(A/'nonflag_HGB40_complete_pipeline_actual_hidden_launches_20261007.json')['launches']
    text=text.replace(needle,"'nonflag_HGB10_actual_controls_main_publication',"+','.join(repr(n) for n in services)+')')
    text=text.replace('(119, 30)):', '(119, 30), (120, 31)):')
    needle="119:'quantile_HGB88_round119_full_registration_v5'}[n]";assert text.count(needle)==1
    text=text.replace(needle,"119:'quantile_HGB88_round119_full_registration_v5',120:'nonflag_HGB40_round120_full_registration'}[n]")
    needle="('quantile88','quantile_HGB88_official_comparison_v5_20261007',88)):";assert text.count(needle)==1
    text=text.replace(needle,"('quantile88','quantile_HGB88_official_comparison_v5_20261007',88),\n        ('nonflag40','nonflag_HGB40_official_comparison_v2_20261007',40)):")
    target=A/'monitor_local_only_runtime_v18_20261007.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8')
    old_h=A/'handoff_local_only_monitor_v17_20261007.py'
    h=substitute(old_h.read_text(encoding='utf8'),{
      'local_only_monitor_v17_actual_handoff_20261007':'local_only_monitor_v18_actual_handoff_20261007',
      'local_only_progress_monitor_v16':'local_only_progress_monitor_v17','local_only_progress_monitor_v17':'local_only_progress_monitor_v18',
      'monitor_local_only_runtime_v16_20261007.py':'monitor_local_only_runtime_v17_20261007.py','monitor_local_only_runtime_v17_20261007.py':'monitor_local_only_runtime_v18_20261007.py',
      'local_only_v17':'local_only_v18','administrative_supersession_local_v17_20261007':'administrative_supersession_local_v18_20261007',
      'passed_actual_idle_observer16_correct117_118_119_recovery_qualification_and_all_science_preserved':'passed_actual_idle_observer17_correct_v5_and120_qualified_only_routes_science_preserved'})
    target_h=A/'handoff_local_only_monitor_v18_20261007.py';assert not target_h.exists();compile(h,str(target_h),'exec');target_h.write_text(h,encoding='utf8')
    create(A/'local_only_monitor_v18_source_preparation_20261007.json',{'status':'compiled_actual_v5_and120_qualification_and40_counts',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,old_h,target_h]},'scientific_workers_stopped':0})

if __name__=='__main__':main()
