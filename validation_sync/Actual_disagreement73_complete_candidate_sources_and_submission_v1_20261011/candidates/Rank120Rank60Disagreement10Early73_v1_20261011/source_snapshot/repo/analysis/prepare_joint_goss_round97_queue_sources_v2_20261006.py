"""Prepare additive queue/observer routes without touching running services."""
from pathlib import Path
import hashlib
import json

A=Path(__file__).resolve().parent

def create(p,value):
    with Path(p).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')

def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    text=(A/'run_dependency_queue_v7_20261006.py').read_text(encoding='utf-8')
    before="'run_goss_reference_quality_with_exact_rank_cache_20261006.py' if job['round'] in (95,96) else"
    after="'run_joint_goss_quality_with_exact_rank_cache_v2_20261006.py' if job['round']==97 else 'run_goss_reference_quality_with_exact_rank_cache_20261006.py' if job['round'] in (95,96) else"
    assert text.count(before)==1;text=text.replace(before,after)
    with (A/'run_dependency_queue_v9_20261006.py').open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    text=(A/'monitor_actual_optimization_progress_v31_20261006.py').read_text(encoding='utf-8')
    text=text.replace('for version in (7, 6, 5, 4):','for version in (9, 8, 7, 6, 5, 4):')
    text=text.replace('for number in (95, 96):','for number in (95, 96, 97):')
    text=text.replace('progress_monitor_v31','progress_monitor_v33').replace('actual_observer_version=31','actual_observer_version=33').replace("'actual_observer_version': 31","'actual_observer_version': 33")
    before="        augment_ready_goss_ownership(value, state, queue)"
    after="""        import qualified_round_recovery_evidence_v3_20261006 as qualification
        joint_pending = qualification.complete_round_evidence(97) is None
        all_pending = sorted(set(value['pending_required_rounds']) | ({97} if joint_pending else set()))
        value.update(pending_required_rounds=all_pending,
            joint_membership_retention_expected_official_records=151,
            joint_membership_retention_pending_rounds=[97] if joint_pending else [],
            joint_membership_retention_new_native_fits=0)
        state.update(pending_required_rounds=all_pending,
            joint_membership_retention_expected_official_records=151,
            joint_membership_retention_pending_rounds=value['joint_membership_retention_pending_rounds'],
            joint_membership_retention_new_native_fits=0)
        augment_ready_goss_ownership(value, state, queue)"""
    assert text.count(before)==1;text=text.replace(before,after)
    with (A/'monitor_actual_optimization_progress_v33_20261006.py').open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    from verify_joint_goss_membership_generators_v2_20261006 import source_paths
    sources=source_paths()+[A/name for name in (
        'joint_goss_membership_generator_preflight_v2_20261006/verification.json',
        'exact_daily_rank_memoization_20261006.py','exact_rank_cache_official_worker_adapter_20261006.py',
        'exact_daily_rank_memoization_preflight_20261006/verification.json',
        'exact_rank_cache_complete_scheme_20261006/verification.json',
        'exact_rank_cache_complete_scheme_v2_20261006/verification.json',
        'exact_rank_cache_windows_scoring_initializer_20261006/verification.json',
        'exact_rank_cache_actual_scoring_adapter_v2_20261006/verification.json',
        'standalone_root_source_adapter_20261005.py','hidden_windows_child_creation_20261006.py',
        'run_reboot_recovery_attempt_20261006.py','run_dependency_queue_v9_20261006.py',
        'monitor_actual_optimization_progress_v33_20261006.py',
        'qualified_round_recovery_evidence_v3_20261006.py',
        'qualified_round_recovery_evidence_v2_20261005.py',
        'qualified_round_recovery_evidence_20261005.py',
        'collect_full_lossless_round_publication_20261006.py',
        'prepare_joint_goss_round97_queue_sources_v2_20261006.py')]
    pins={str(p):sha(p) for p in dict.fromkeys(sources)}
    create(A/'joint_goss_membership_quality_run_v2_20261006.json',{
        'status':'frozen_before_actual_complete_output_quality','round':97,'explicit_parent_round':95,
        'required_official_records':151,'waves':[378,379,380],'wave_arm_counts':[73,24,54],
        'original67_through96_retained':True,'input_sha256':pins,'new_native_fits':0,
        'single_scoring_worker':True,'test_labels_read':False,
        'actual_dispatch_and_complete_quality_still_pending':True})
    create(A/'joint_goss_membership_round97_previous_run_v2_20261006.json',{
        'name':'round97','original_script':str(A/'run_training_round97_v2_pipeline.py'),
        'original_arguments':[],'input_sha256':pins,
        'recovery_driver_sha256':sha(A/'run_reboot_recovery_attempt_20261006.py'),
        'test_labels_read':False,'new_native_fits':0})
    print('Frozen full round97 run and additive queue8/observer32 sources; no services replaced.',flush=True)

if __name__=='__main__':main()
