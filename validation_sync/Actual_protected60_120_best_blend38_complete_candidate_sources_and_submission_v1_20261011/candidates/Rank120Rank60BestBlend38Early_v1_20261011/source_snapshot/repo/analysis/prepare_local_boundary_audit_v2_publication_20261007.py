"""Queue actual audit and cleanup evidence after the current121 main writer finishes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    old=A/'publish_local_boundary_audit_v1_20261007.py';new=A/'publish_local_boundary_audit_v2_20261007.py'
    text=old.read_text(encoding='utf8').replace('local_optimization_boundary_audit_v1_20261007','local_optimization_boundary_audit_v2_20261007').replace('local_boundary_audit_v1_github_20261007','local_boundary_audit_v2_github_20261007').replace('validation_sync/local_boundary_audit_v1_20261007','validation_sync/local_boundary_audit_v2_20261007')
    text=text.replace("closed('local_only_monitor_v8_actual_handoff')","closed('local_only_monitor_v21_exact_idle_handoff')").replace("closed('CPU_MLP44_round110_full_registration')","closed('nonflag_Ridge40_round121_full_registration_v1')")
    text=text.replace('verified_completed_recent_scopes_with_live_open_directions_not_global_exhaustion','verified_recent_closed_scopes_selected_sealed_files_and_live_open_directions_not_global_exhaustion')
    text=text.replace("'latest_complete_round':110,'best_origin_round':106", "'latest_complete_round':proof['latest_complete_round'],'best_origin_round':proof['selected_best_origin_round']")
    text=text.replace("'更新第110轮后有限优化范围及仍开放方向的资源证据'","'上传本机有限优化范围、候选封存重哈希及有界清理验证'")
    needle="    pins = {**proof['input_sha256'], **{str(p): sha(p) for p in sources}}";assert text.count(needle)==1
    text=text.replace(needle,"""    sources += [A/'local_only_monitor_v21_actual_handoff_20261007/verification.json',A/'local_only_monitor_v21_source_preparation_20261007.json',
        A/'bounded_closed_score_cleanup_v2_source_preparation_20261007.json',A/'bounded_frozen_SHA_bindings_20261007.py',
        A/'prepare_bounded_closed_score_cleanup_v2_20261007.py',A/'plan_closed_local_score_scratch_cleanup_v2_20261007.py',
        A/'closed_local_score_scratch_cleanup_20261007/read_only_scan_resource_stop.json',
        *list((A/'bounded_frozen_SHA_bindings_preflight_20261007').glob('*.json'))]
    cleanup=A/'closed_local_score_scratch_cleanup_v2_20261007'
    assert (cleanup/'verification.json').exists(), 'Require actual completed cleanup evidence before publication'
    sources += list(cleanup.glob('*.json')) + list(cleanup.glob('*.jsonl'))
    sources=list(dict.fromkeys(sources))
"""+needle)
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    create(A/'local_boundary_audit_v2_publication_source_preparation_20261007.json',{'status':'compiled_serial_main_publication_after121_with_actual_audit_and_cleanup_gate',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),old,new)},'new_quality_scores':0,'test_labels_read':False})
    print({'status':'compiled_serial_publisher'},flush=True)
if __name__=='__main__':main()
