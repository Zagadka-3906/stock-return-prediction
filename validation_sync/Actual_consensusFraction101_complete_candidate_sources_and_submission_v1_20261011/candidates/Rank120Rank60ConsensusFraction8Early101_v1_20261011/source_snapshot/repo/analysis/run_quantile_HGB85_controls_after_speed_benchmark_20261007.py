"""Run full quantile controls after the local scoring benchmark releases its heap."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
def main():
    folder=A/'service_owned_workflows_20261006/cached_official_spearman_full12_benchmark'
    while owned(read(folder/'native_launch.json')):time.sleep(10)
    # Controls are useful even if a proposed speed adapter failed equivalence.
    assert (folder/'service_execution.json').is_file()
    from verify_quantile_HGB88_transform_20261007 import main as actual
    actual()
if __name__=='__main__':main()
