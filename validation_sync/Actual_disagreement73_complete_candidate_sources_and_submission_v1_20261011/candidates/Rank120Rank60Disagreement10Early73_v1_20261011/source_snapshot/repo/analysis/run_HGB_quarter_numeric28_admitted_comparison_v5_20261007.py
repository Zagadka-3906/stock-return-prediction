"""Require actual118 admission and25-control main receipt before any28 official score."""
from pathlib import Path
import sys
import time
import runpy
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned

def main():
    for name in ('HGB_quarter_numeric28_round118_source_admission_v5','HGB_quarter_numeric28_full25_controls_main_publication_v5'):
        folder=A/'service_owned_workflows_20261006'/name
        while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
        assert read(folder/'service_execution.json')['status']=='passed',name
    proof=read(A/'HGB_quarter_numeric28_round118_source_admission_v5_20261007.json')
    assert proof['status']=='passed_actual25_controls_and24_prospective118_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    runpy.run_path(str(A/'run_HGB_quarter_numeric28_official_comparison_v5_20261007.py'),run_name='__main__')

if __name__=='__main__':main()
