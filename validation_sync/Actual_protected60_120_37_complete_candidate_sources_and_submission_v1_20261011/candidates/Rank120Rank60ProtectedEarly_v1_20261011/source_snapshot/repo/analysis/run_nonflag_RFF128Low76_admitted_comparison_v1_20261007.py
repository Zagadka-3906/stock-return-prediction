"""Run official comparisons only after real complete source admission and main controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned

def main():
    for name in ('nonflag_RFF128Low76_round126_source_admission_v1','nonflag_RFF128Low76_full37_controls_main_publication_v1'):
        f=A/'service_owned_workflows_20261006'/name
        while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(10)
        assert read(f/'service_execution.json')['status']=='passed',name
    proof=read(A/'nonflag_RFF128Low76_round126_source_admission_v1_20261007.json')
    assert proof['status']=='passed_actual73_controls_and24_prospective126_complete_source_schema_paths_and_graph_routes'
    assert len(proof['baseline_gain_regressions'])==9 and len(proof['graph_metadata_controls'])==24
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    from run_nonflag_RFF128Low76_official_comparison_v1_20261007 import main as actual
    actual()
if __name__=='__main__':main()
