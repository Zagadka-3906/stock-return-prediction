from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
oldname='recovery64_StockRank10Embedding192_complete48_family_v1_20261011';newname='recovery83_StockRank10Embedding192_complete48_family_v1_20261011'
folder=A/'service_owned_workflows_20261006'/oldname;assert not owned(read(folder/'native_launch.json')) and 'Unexpected staged delta' in read(folder/'service_execution.json')['failure']
from stock_rank10_embedding192_storage_v1_20261011 import OUTPUTS
for logical,physical in OUTPUTS.items():assert not logical.exists() and not physical.exists()
assert not (A/'StockRank10Embedding192_complete_family_v1_20261011').exists()
control=A/'actual_ancestor_index_guard83_positive_negative_v1_20261011.json';assert read(control)['negative']['actual_private_staged_change_rejected']
oldproof=A/'actual_current_completed_parents71_child_propagation_admission_v1_20261011.json';d=read(oldproof);children={};outputs=[]
for original,oldwrapper in d['child_driver_wrappers'].items():
 p=A/(Path(original).stem+'_ancestor_guard83_child.py');code='from route_current_parents71_ancestor_guard83_v1_20261011 import execute\nif __name__=="__main__":execute('+repr(oldwrapper)+')\n';ast.parse(code);assert not p.exists();p.write_text(code,encoding='utf8');outputs.append(p);children[original]=p.name
wrapper=A/'run_StockRank10Embedding192_complete_family_current_main83_wrapper_v1_20261011.py';code='from route_current_parents71_ancestor_guard83_v1_20261011 import execute\nif __name__=="__main__":execute("run_StockRank10Embedding192_complete_family_v1_20261011_completed_parents71_wrapper.py")\n';ast.parse(code);assert not wrapper.exists();wrapper.write_text(code,encoding='utf8')
proof=A/'actual_ancestor_guard83_future_scope_admission_v1_20261011.json';create(proof,{'status':'frozen_current_main_shared_ref_index_sync_only_exact_published_ancestor_guard_actual_positive_and_private_negative_passed_original_scientific_scripts_and_48_scope_unchanged','input_sha256':{str(p):sha(p) for p in [Path(__file__),control,oldproof,A/'verified_ancestor_only_current_main_index_guard83_v1_20261011.py',A/'route_current_parents71_ancestor_guard83_v1_20261011.py',wrapper,*outputs]},'service_alias_updates':{oldname:newname},'child_driver_wrappers':children,'original_failed192_preserved':True,'original_normalization_and_native14_not_repeated':True,'new_scientific_scores':0,'new_training':0})
assert allowed();r=start_service(newname,wrapper.name,[],{str(wrapper):sha(wrapper),str(proof):sha(proof)});create(A/'recovery83_StockRank10Embedding192_complete48_family_activation_v1_20261011.json',r)
print({'actual_failed192_family_resumed_only':True,'completed_normalization_native14_reused':True,'all_original_future_children_guard83_admitted':len(children)},flush=True)
