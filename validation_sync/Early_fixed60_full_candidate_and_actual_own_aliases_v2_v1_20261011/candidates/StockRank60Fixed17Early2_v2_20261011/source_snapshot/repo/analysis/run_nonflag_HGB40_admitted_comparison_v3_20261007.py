"""Wait for full119 source admission and actual85 main evidence before official scoring."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned
def main():
    for name in ('nonflag_HGB40_round120_source_admission_v3','nonflag_HGB40_full37_controls_main_publication_v3'):
        f=A/'service_owned_workflows_20261006'/name
        while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(10)
        assert read(f/'service_execution.json')['status']=='passed',name
    proof=read(A/'nonflag_HGB40_round120_source_admission_v3_20261007.json')
    assert proof['status']=='passed_actual37_controls_and24_prospective120_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    from run_nonflag_HGB40_official_comparison_v3_20261007 import main as actual
    actual()
if __name__=='__main__':main()
