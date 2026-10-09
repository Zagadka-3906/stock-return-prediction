from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
def main():
    p=read(A/'BF16Seed10_80_prospective_routes_v1_20261009.json')
    assert (p['prospective_sources'],len(p['graph_controls']),len(p['baseline_controls']),len(p['physical_model_count_absolute_weight_sort_controls']))==(56,2100,21,14)
    for f,d in p['input_sha256'].items():assert sha(f)==d,f
    print({'passed_source_routes':56,'passed_graphs':2100,'new_quality_scores':0},flush=True)
if __name__=='__main__':main()
