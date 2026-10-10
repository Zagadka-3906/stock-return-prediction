"""Serialize all92 raw official records after complete full107 receipt recovery."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, owned


def main():
    service = A / 'service_owned_workflows_20261006/round107_full_QA_receipt_closure'
    while not (service / 'native_launch.json').exists():
        time.sleep(15)
    row = read(service / 'native_launch.json')
    while owned(row):
        time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    assert read(A / 'optimization_20261003_r107/full_registration_execution.json')['status'] == 'passed'
    from publish_single_host_rank36_evidence_20261007 import main as publish
    publish('scores')


if __name__ == '__main__':
    main()
