"""Verify actual executed admission and all source hashes; do not fabricate a predecessor."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
proof=read(A/'quantile_HGB88_round119_source_admission_v6_20261007.json')
assert proof['status']=='passed_actual85_controls_and24_prospective119_complete_source_schema_paths_and_graph_routes'
for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
print({'status':'passed_actual_executed119_admission_and_all_source_hashes'})
