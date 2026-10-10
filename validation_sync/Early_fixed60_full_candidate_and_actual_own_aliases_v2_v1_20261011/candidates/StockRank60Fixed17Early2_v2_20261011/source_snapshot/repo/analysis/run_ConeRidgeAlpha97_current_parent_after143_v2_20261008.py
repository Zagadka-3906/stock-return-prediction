"""Correct missing dependency wait; original current-parent mathematics stays byte-identical."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    originals=[A/'verify_ConeRidgeAlpha97_current_parent_v1_20261008.py',
               A/'service_owned_workflows_20261006/ConeRidgeAlpha97_current_parent_controls_v1_20261008/service_execution.json']
    assert read(originals[1])['status']=='failed'
    pins={str(p):sha(p) for p in [Path(__file__),*originals]}
    for name in ('ConeRidgeFine68_round143_full_registration_v2_20261008',
                 'ConeRidgeAlpha97_parent134_historical_controls_v1_20261008'):
        folder=A/'service_owned_workflows_20261006'/name
        while owned(read(folder/'native_launch.json')):time.sleep(10)
        assert read(folder/'service_execution.json')['status']=='passed',name
    assert read(A/'optimization_20261003_r143/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round143_receipt.json')['status']=='pushed_and_remote_head_verified'
    create(A/'ConeRidgeAlpha144_current_parent_dependency_recovery_v2_20261008.json',{
        'status':'passed_exact_missing_parent143_dependency_wait_before_unchanged_actual97_controls',
        'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    from verify_ConeRidgeAlpha97_current_parent_v1_20261008 import main as original
    original()
if __name__=='__main__':main()
