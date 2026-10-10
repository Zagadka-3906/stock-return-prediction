"""Resolve the actually running504 scientific queue without changing frozen188 scientific sources."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha

def main():
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    assert checks.allowed()
    proof=A/'long188_actual_scientific_queue_routes_v2_20261011.json';data=read(proof)
    for p,d in data['input_sha256'].items():assert sha(p)==d,p
    previous=checks.closed
    def actual_closed(name):return previous(data['dependency_aliases'].get(name,name))
    checks.closed=actual_closed
    factory=importlib.import_module('prepare_StockRank20LongEmbedding188_complete48_pipeline_v1_20261011')
    original=factory.source_paths
    factory.source_paths=lambda:list(dict.fromkeys([*original(),Path(__file__),proof,A/'recover_long188_actual_queue_dependency_v2_20261011.py']))
    family=importlib.import_module('run_StockRank20LongEmbedding188_complete_family_v1_20261011')
    family.closed=actual_closed
    family.main()

if __name__=='__main__':main()
