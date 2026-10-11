"""Wait for real source admission and controls publication before importing340 science."""
from pathlib import Path
import sys
import time
import runpy
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    closed('weighted_HGB340_round117_source_admission')
    closed('weighted_HGB340_full337_controls_main_publication')
    proof=read(A/'weighted_HGB340_round117_source_admission_20261007.json')
    assert proof['status']=='passed_actual337_controls_and24_prospective117_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    runpy.run_path(str(A/'run_flagged_HGB_weighted_quarters340_official_comparison_v3_20261007.py'),run_name='__main__')

if __name__=='__main__':main()
