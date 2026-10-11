from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
old=A/'prepare_Rank60TwoSeedProtected205_complete39_pipeline_v1_20261011.py'
s=old.read_text(encoding='utf8')
s=s.replace("PROOF='rank60_two_seed_protected205_full_execution_sources_admission_v1_20261011.json'","PROOF='rank60_two_seed_protected205_full_execution_sources_admission_v2_20261011.json'")
s=s.replace("EXTRAS[16]='rank60_two_seed_protected37_early_sources_admission_v2_20261011.json'","EXTRAS[16]='rank60_two_seed_after183_protected37_predeclared_sources_admission_v1_20261011.json'")
s=s.replace("EXTRAS += [", "NAMES=[n.replace('_v1_20261011','_v2_20261011') for n in NAMES]\nEXTRAS=[n.replace('_v1_20261011','_v2_20261011') if i<12 or i==15 else n for i,n in enumerate(EXTRAS)]\nEXTRAS += [")
s=s.replace('shared_live_report_scope205_tuple_controls_v1_20261011','shared_live_report_scope205_tuple_controls_v2_20261011').replace('共享榜对象205精确作用域_v1_20261011','共享榜对象205精确作用域_v2_20261011')
s=s.replace("for i,name in [(2,'optimize_training_round205.py'),(3,'finalize_training_round205.py')]:outputs.append(save(A/name,'from '+Path(NAMES[i]).stem+' import *\\n'))", "# Existing canonical v1 files remain immutable. The fresh registration process binds v2 modules explicitly.")
needle="  outputs.append(save(A/aliases[name],text))"
repair="""  if name==template.EXTRAS[6]:
   text=text.replace('    protocol=register();', '    import importlib\\n    sys.modules["optimize_training_round205"]=importlib.import_module("'+Path(NAMES[2]).stem+'")\\n    sys.modules["finalize_training_round205"]=importlib.import_module("'+Path(NAMES[3]).stem+'")\\n    protocol=register();')
  text=text.replace("'stock_rank60seed10_embedding_small512_BF16_bank6_v1_20261011':'actual_StockRank120EmbeddingSmall512_full5_independent_location_v1_20261011.json'", "'stock_rank60seed10_embedding_small512_BF16_bank6_v1_20261011':'actual_StockRank60Seed10EmbeddingSmall512_full5_independent_location_v1_20261011.json'")
"""
s=s.replace(needle,repair+needle)
s=s.replace('actual_rank60_two_seed_protected39_after204_normalization_v1_20261011','actual_rank60_two_seed_protected39_after204_normalization_v2_20261011').replace('actual_rank60_two_seed_protected39_selected_native14_v1_20261011','actual_rank60_two_seed_protected39_selected_native14_v2_20261011').replace('Rank60TwoSeedProtected205_complete39_family_v1_20261011','Rank60TwoSeedProtected205_complete39_family_v2_20261011')
p=A/'prepare_Rank60TwoSeedProtected205_complete39_pipeline_v2_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
create(A/'actual205_partial_factory_prospective_repair_admission_v2_20261011.json',{'status':'partial_v1_factory_preserved_no_v1_scientific_services_started_new_exclusive_v2_factory_corrects_missing_protocol_pointer_and_seed10_control_pointer','input_sha256':{str(old):sha(old),str(p):sha(p)},'new_fits_or_scores':0})
print(p,flush=True)
