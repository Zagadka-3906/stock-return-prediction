"""Reconcile actual complete162 success after a strictly identified process-local cleanup error."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from run_protected162_complete_family_v1_20261010 import junction
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();base=A/'service_owned_workflows_20261006'
    original=base/'TailProtected162_round162_full_registration_v1_20261010'
    assert not owned(read(original/'native_launch.json'))
    failed=read(original/'service_execution.json');assert failed['status']=='failed' and failed['failure']=='AssertionError: '
    trace=(original/'stderr.log').read_text(encoding='utf8');assert "assert ranking.main is namespace['main'];ranking.main=original" in trace and trace.rstrip().endswith('AssertionError')
    scope=read(A/'optimization_20261003_r162/provenance_scope_execution.json');assert scope['status']=='passed'
    for p,d in scope['input_sha256'].items():assert sha(p)==d,p
    done=read(A/'optimization_20261003_r162/full_registration_execution.json');assert done['status']=='passed' and done['existing_official_scores_registered']==76
    receipt=read(A/'github_validation_sync_main_20261005/round162_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==76 and receipt['connected_records']==15728
    candidate=ROOT/'candidates/optimization_20261003_r162';manifest=read(candidate/'manifest.json');assert manifest['status']=='passed'
    for relative,info in manifest['files'].items():assert sha(candidate/relative)==info['sha256'],relative
    verification=read(candidate/'verification.json');assert verification['rows']==1599600 and verification['model_reload_bit_identical'] and verification['cold80_day_prefix_bit_identical']
    replacement=base/'actual_complete162_post_publication_cleanup_reconciliation_v1_20261010'
    for name in ('TailProtected162_round162_full_registration_v1_20261010','TailProtected162_complete76_family_v1_20261010'):
        source=base/name;assert not owned(read(source/'native_launch.json'))
        archive=base/(name+'_original_cleanup_failure_evidence_v1_20261010');assert not archive.exists();source.rename(archive);junction(source,replacement)
    alias=base/'ReusedNN162Quality19_round162_full_registration_v1_20261009';assert not alias.exists();junction(alias,replacement)
    create(A/'actual_complete162_post_publication_cleanup_reconciliation_v1_20261010.json',{'status':'passed_complete162_candidate_all_manifest_files_full_QA73_and_verified_main_receipt_rehashed_after_process_local_cleanup_failure','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_service_failure':failed,'main_receipt':receipt,'manifest_files_rehashed':len(manifest['files']),'scope_input_files_rehashed':len(scope['input_sha256']),'new_quality_scores':0,'new_inference':False,'new_native_fits':0,'original_failures_preserved':True,'test_labels_read':False})
if __name__=='__main__':main()
