"""Revalidate the actual pre-quality40-route result without re-running immutable file creation."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha

def main():
    p=read(A/'BF16Medium78_prospective_routes_v1_20261009.json')
    assert p['prospective_sources']==40 and len(p['graph_controls'])==1500
    assert len(p['baseline_controls'])==15 and len(p['physical_model_count_absolute_weight_sort_controls'])==10
    for f,d in p['input_sha256'].items():assert sha(f)==d,f
    import prepare_BF16Medium78_round153_sources_v1_20261009 as g,hashlib
    out={str(y):{name:hashlib.sha256(s.encode()).hexdigest() for name,s in g.generate(y).items()} for y in (148,149,150,151,152)}
    assert out==p['generated_source_sha256']
    print({'actual_proof_revalidated':True,'new_route_execution_claimed':False,'sources':40},flush=True)

if __name__=='__main__':main()
