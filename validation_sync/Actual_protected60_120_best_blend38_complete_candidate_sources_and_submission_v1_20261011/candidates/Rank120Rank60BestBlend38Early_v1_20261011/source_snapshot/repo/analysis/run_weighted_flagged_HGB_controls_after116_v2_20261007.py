"""Run full337 controls after full116 closes, preserving memory for its original QA."""
from pathlib import Path
import runpy
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned

def main():
    service=A/'service_owned_workflows_20261006/flagged_HGB88_round116_full_registration'
    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)
    assert read(service/'service_execution.json')['status']=='passed'
    assert read(A/'optimization_20261003_r116/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round116_receipt.json')['actual_full_QA_version']==27
    hook=A/'service_owned_workflows_20261006/weighted_flagged_HGB_native_hook_preflight_v2'
    while not (hook/'native_launch.json').exists() or owned(read(hook/'native_launch.json')):time.sleep(15)
    assert read(hook/'service_execution.json')['status']=='passed'
    proof=read(A/'weighted_flagged_HGB_native_hook_preflight_v2_20261007/verification.json')
    assert len(proof['records'])==28 and proof['status']=='passed_actual28_historical603_weighted_HGB_unique_native_independent_and_whole_day_prefix_controls'
    runpy.run_path(str(A/'verify_flagged_HGB_weighted_quarters340_transform_20261007.py'),run_name='__main__')

if __name__=='__main__':main()
