from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed();closed('actual_completed_weight84_namespace_bridge90_v1_20261011')
old=A/'run_publish_actual_completed_consensus8_all_records81_v1_20261011.py';s=old.read_text(encoding='utf8')
for before,after in [('actual_rank120_rank60_after183_consensus8_screen80_v1_20261011','actual_completed_weight84_namespace_bridge90_v1_20261011'),('StockRank120Rank60_after183_consensus8_screen80_v1_20261011','StockRank120Rank60_after183_consensusWeight8_screen84_v1_20261011'),('rank120_rank60_consensus8_predeclared_sources80_v1','rank120_rank60_consensusWeight8_predeclared_sources84_v1'),('Rank120Rank60Consensus_after183_actual8_81','Rank120Rank60ConsensusWeight_after183_actual8_96')]:s=s.replace(before,after)
p=A/'run_publish_completed_weight84_actual8_early96_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');name='actual_completed_weight84_actual8_early96_main_v1_20261011';r=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r)
