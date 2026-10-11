"""Wait for full119 source admission and actual85 main evidence before official scoring."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned
def main():
    for name in ('quantile_HGB88_round119_source_admission_v4','quantile_HGB88_full85_controls_main_publication_v4'):
        f=A/'service_owned_workflows_20261006'/name
        while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(10)
        assert read(f/'service_execution.json')['status']=='passed',name
    proof=read(A/'quantile_HGB88_round119_source_admission_v4_20261007.json')
    assert proof['status']=='passed_actual85_controls_and24_prospective119_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    from run_quantile_HGB88_official_comparison_v4_20261007 import main as actual
    actual()
if __name__=='__main__':main()
