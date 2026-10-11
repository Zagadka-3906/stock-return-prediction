from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed();source=A/'run_publish_completed_weight84_actual8_early96_v1_20261011.py'
for kind,number,prefix in [('consensusFraction8',100,'ConsensusFraction_after183_actual8_114'),('consensusFractionWeight8',108,'ConsensusFractionWeight_after183_actual8_115')]:
 s=source.read_text(encoding='utf8')
 for old,new in [('actual_completed_weight84_namespace_bridge90_v1_20261011',f'actual_rank120_rank60_after183_{kind}_screen{number}_v1_20261011'),('StockRank120Rank60_after183_consensusWeight8_screen84_v1_20261011',f'StockRank120Rank60_after183_{kind}_screen{number}_v1_20261011'),('rank120_rank60_consensusWeight8_predeclared_sources84_v1',f'rank120_rank60_{kind}_predeclared_sources{number}_v1'),('Rank120Rank60ConsensusWeight_after183_actual8_96','Rank120Rank60'+prefix)]:s=s.replace(old,new)
 p=A/f'run_publish_completed_{kind}_actual8_early114_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');name=f'actual_completed_{kind}_actual8_early114_main_v1_20261011';assert allowed();r=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r)
