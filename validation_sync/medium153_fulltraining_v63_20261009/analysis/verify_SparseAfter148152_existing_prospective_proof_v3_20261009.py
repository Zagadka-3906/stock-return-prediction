from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
proof=A/'SparseAfter14829_prospective_routes_v1_20261009.json';p=read(proof)
assert p['actual_prospective_sources']==32 and p['actual_graph_controls']==200
for path,digest in p['input_sha256'].items():assert sha(path)==digest,path
assert set(p['generated_source_sha256'])=={'148','149','150','151'}
for c in p['graph_controls']:assert c['all_complete_parent_graph_values_preserved_once']
create(A/'SparseAfter148152_actual_prospective_scope_v3_20261009.json',{'status':'passed_actual152_32_sources200_graphs_fixed148_and_comparison148to151',
 'input_sha256':{str(Path(__file__)):sha(__file__),str(proof):sha(proof)},'inherited_old_status_label_retained_in_raw_proof':p['status'],
 'actual_round':152,'actual_stage_base':148,'actual_sources':32,'actual_graph_controls':200,'new_quality_scores':0})
print('Actual152 prospective proof scope and all hashes verified.')
