"""Wait for passed quantile admission before any20 native fitting."""
from pathlib import Path
import sys
import time
import runpy
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned

def main():
    folder=A/'service_owned_workflows_20261006/quantile_HGB_native_bank20_source_admission'
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    runpy.run_path(str(A/'train_quantile_HGB_native_bank20_20261007.py'),run_name='__main__')

if __name__=='__main__':main()
