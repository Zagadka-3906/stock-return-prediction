from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
original=A/'run_rank120_rank60_after183_consensus8_screen80_v1_20261011.py'
s=original.read_text(encoding='utf8');node=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='cases')
cases=ast.literal_eval(node.body[0].value)[:2]
cases += [dict(cases[1],disagreement_penalty=k,weight=w) for k,w in [(.5,.016),(.5,.024),(.5,.04),(.5,.048),(.75,.024),(.75,.04)]]
lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['def cases():\n    return '+repr(cases)+'\n'];s=''.join(lines)
for old,new in [('StockRank120Rank60_after183_consensus8_screen80_v1','StockRank120Rank60_after183_consensusWeight8_screen84_v1'),('rank120_rank60_consensus8_predeclared_sources80_v1','rank120_rank60_consensusWeight8_predeclared_sources84_v1'),('passed8_consensus80','passed8_consensusWeight84')]:s=s.replace(old,new)
p=A/'run_rank120_rank60_after183_consensusWeight8_screen84_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
proof=A/'rank120_rank60_consensusWeight8_predeclared_sources84_v1_20261011.json'
create(proof,{'status':'frozen_before_scoring_six_uncovered_weights_with_two_exact_references','cases':cases,'input_sha256':{str(x):sha(x) for x in [Path(__file__),original,p,A/'rank120_rank60_consensus_raw_signal80_v1_20261011.py',A/'actual_consensus8_pointwise_CPU_controls80_v1_20261011.json']},'test_labels_read':False,'new_fits':0})
oldqueue=A/'run_original191_then_all_current_science_priority80_then_original48_v1_20261011.py'
tree=ast.parse(oldqueue.read_text(encoding='utf8'));fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');assignment=next(n for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='wrappers' for t in n.targets));mapping=ast.literal_eval(assignment.value)
remaining=read(A/'actual_current_completed_parents71_child_propagation_admission_v1_20261011.json')['remaining_tasks'][3:];assert len(remaining)==45
wrapped={}
for name,_ in remaining:
 originaldriver=mapping[name];driver=A/(Path(originaldriver).stem+'_ancestor_guard84_wrapper.py');assert not driver.exists();driver.write_text('from route_current_parents71_ancestor_guard83_v1_20261011 import execute\nif __name__=="__main__":execute('+repr(originaldriver)+')\n',encoding='utf8');wrapped[name]=driver.name
q=A/'run_original_remaining45_after_recovery83_v84_20261011.py'
q.write_text('from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom run_dependency_queue_v3_20261006 import read,sha,create\nfrom prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed\nfrom start_fast_completed_owned_service_v1_20261011 import start_service\nassert allowed()\nclosed("recovery83_StockRank10Embedding192_complete48_family_v1_20261011")\nfor name,driver in '+repr(list(wrapped.items()))+':\n assert allowed();p=A/driver;proof=A/"actual_ancestor_guard83_future_scope_admission_v1_20261011.json"\n r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof),str(A/"route_current_parents71_ancestor_guard83_v1_20261011.py"):sha(A/"route_current_parents71_ancestor_guard83_v1_20261011.py")});create(A/(name+"_actual_guard84_activation.json"),r);closed(name)\nprint("Original remaining45 complete; final audit remains separate",flush=True)\n',encoding='utf8');ast.parse(q.read_text(encoding='utf8'))
admission=A/'actual_weight84_and_remaining45_scope_admission_v1_20261011.json';create(admission,{'status':'unchanged_original45_tasks_after_actual192_only_and_six_new_TRAIN_weight_scores','remaining_tasks':remaining,'wrappers':wrapped,'input_sha256':{str(x):sha(x) for x in [Path(__file__),proof,p,q,*[A/v for v in wrapped.values()]]},'previous_failed192_not_rewritten':True,'test_labels_read':False})
for name,driver in [('actual_rank120_rank60_after183_consensusWeight8_screen84_v1_20261011',p),('actual_original_remaining45_after_recovery83_v84_20261011',q)]:
 assert allowed();r=start_service(name,driver.name,[],{str(driver):sha(driver),str(admission):sha(admission)});create(A/(name+'_activation.json'),r)
