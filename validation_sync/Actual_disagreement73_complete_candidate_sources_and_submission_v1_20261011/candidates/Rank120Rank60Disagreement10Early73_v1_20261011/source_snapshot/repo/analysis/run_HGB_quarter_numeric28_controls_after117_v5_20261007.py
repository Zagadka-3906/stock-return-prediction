"""Preserve memory for full117 QA; run25 controls after both actual main publications."""
from pathlib import Path
import sys
import time
import runpy
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned

def main():
    for name in ('weighted_HGB340_round117_full_registration_v2','HGB_quarter_numeric_audit_main_publication_after117_v5'):
        folder=A/'service_owned_workflows_20261006'/name
        while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
        assert read(folder/'service_execution.json')['status']=='passed',name
    assert read(A/'optimization_20261003_r117/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round117_receipt.json')['actual_full_QA_version']==28
    runpy.run_path(str(A/'verify_HGB_quarter_numeric28_transform_v5_20261007.py'),run_name='__main__')

if __name__=='__main__':main()
