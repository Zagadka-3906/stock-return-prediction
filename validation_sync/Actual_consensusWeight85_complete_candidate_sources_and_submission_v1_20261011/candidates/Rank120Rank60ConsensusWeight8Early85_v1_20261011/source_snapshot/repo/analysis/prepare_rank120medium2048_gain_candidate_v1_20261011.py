"""Complete candidate path for the new120 capacity: dispatch only on an official TRAIN gain."""
from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def changed(s):
 for old,new in [('stock_rank60medium','stock_rank120medium'),('StockRank60Medium','StockRank120Medium'),('rank60medium2048','rank120medium2048'),('rank60mean','rank120mean'),('y_rank_60mean','y_rank_120mean'),('股票60日更大容量','股票120日更大容量'),('60日更大容量','120日更大容量')]:s=s.replace(old,new)
 # The qualifying worker must never write another family's location pointer.
 s=s.replace('actual_stock_rank60_direct_embedding35_selected_native14_location','actual_stock_rank120medium_best33_selected_native14_location')
 return s

def main():
 assert allowed()
 names=['verify_stock_rank60medium_best33_native14_v2_20261011.py','prepare_StockRank60MediumBest33Early_selected_candidate_v2_20261011.py','run_StockRank60MediumBest33Early_selected_candidate_feature_cache_v2_20261011.py','seal_StockRank60MediumBest33Early_selected_candidate_v2_20261011.py','seal_StockRank60MediumBest33Early_selected_candidate_v3_20261011.py','stock_rank60medium_best33_early_storage_v2_20261011.py','rank60medium2048_early_candidate_recipes_v1_20261011.py','run_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011.py','publish_actual_rank60medium2048_best33_complete_candidate_main_v1_20261011.py','prepare_verified_rank60medium2048_best33_alternate_submission_delivery_v1_20261011.py']
 outputs=[]
 for name in names:
  p=A/name;q=A/changed(name);s=changed(p.read_text(encoding='utf8'));ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8',newline='\n');outputs.append(q)
 protocol=A/'stock_rank120medium2048_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json'
 cpu=A/'stock_rank120medium_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json';assert len(read(cpu)['records'])==12
 proof=A/'rank120medium2048_best33_full_candidate_sources_admission_v1_20261011.json'
 create(proof,{'status':'predeclared_H120_medium_complete36_native14_cold14_prefit7_independent_full_replay_cold80_main_delivery_gain_only','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in names],*outputs,protocol,cpu]},'expected_source_score_records':33,'expected_native_cases':14,'expected_cold_cases':14,'expected_prefit_refusals':7,'maximum_new_models':1,'complete_parent_native_independent_reload_and_cold80_required':True,'candidate_dispatch_only_if_strictly_higher_official_TRAIN_S':True,'test_labels_read':False,'new_fits':0,'new_scores':0})
 imported=[]
 for q in outputs[:9]:
  # The delivery script intentionally waits at module scope; do not import it here.
  importlib.import_module(q.stem);imported.append(q.name)
 create(A/'rank120medium2048_full_candidate_runtime_import_admission_v1_20261011.json',{'status':'passed_actual9_runtime_module_imports_no_fits_scores_or_inference','modules':imported,'input_sha256':{str(proof):sha(proof),str(Path(__file__)):sha(__file__)},'new_fits':0,'new_scores':0})
 for name,p in [('actual_rank120medium2048_gain_selected_full_candidate_queue_v1_20261011',outputs[7]),('actual_rank120medium2048_best33_complete_candidate_main_v1_20261011',outputs[8]),('actual_verified_rank120medium2048_best33_alternate_delivery_v1_20261011',outputs[9])]:
  assert allowed();i=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),i)
 print('H120 medium all36 candidate/reload/independent/cold80, main and E delivery predeclared; no candidate inferred yet',flush=True)

if __name__=='__main__':main()
