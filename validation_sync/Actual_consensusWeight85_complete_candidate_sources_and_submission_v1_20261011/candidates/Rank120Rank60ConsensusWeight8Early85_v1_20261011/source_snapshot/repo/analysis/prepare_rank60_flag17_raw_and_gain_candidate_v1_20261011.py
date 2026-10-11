"""Explore flag-only ranking with an existing verified bank; original official all8 scoring remains mandatory."""
from pathlib import Path
import sys,ast,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def save(p,s):
 ast.parse(s);assert not p.exists(),p;p.write_text(s,encoding='utf8',newline='\n');return p

def changed(s):
 for old,new in [('stock_rank60medium_best33','stock_rank60_flag17'),('StockRank60MediumBest33Early','StockRank60FlagOnlyBest17Early'),('rank60medium2048','rank60_flag17'),('stock_rank60medium_embedding','stock_rank60_embedding'),('stock_rank60medium_actual','stock_rank60_actual'),('StockRank60MediumEmbeddingMedium2048','StockRank60EmbeddingSmall512'),('medium2048','small512'),('股票60日更大容量最佳33项','股票60日涨停股最佳17项'),('60日更大容量最佳33项','60日涨停股最佳17项')]:s=s.replace(old,new)
 # Replace standalone score/control cardinalities only; this does not affect any model configuration.
 for old,new in [(33,17),(32,16),(96,48)]:s=re.sub(r'(?<!\d)'+str(old)+r'(?!\d)',str(new),s)
 for old,new in [('selected_best33','selected_best17'),('actual33','actual17'),('all33','all17'),('All33','All17'),('best33','best17'),('33_TRAIN','17_TRAIN')]:s=s.replace(old,new)
 s=s.replace('stock_rank60_direct_embedding35_selected_native14_location','stock_rank60_flag17_selected_native14_location')
 s=s.replace('StockRank60EmbeddingSmall512_after183_direct_allocation33_screen','StockRank60FlagOnly_after183_direct17_screen')
 s=s.replace('actual_stock_rank60_embedding_after183_direct_allocation33','actual_stock_rank60_flag17_after183_direct17')
 return s

def main():
 assert allowed()
 source=A/'run_stock_rank60_embedding_after183_direct_allocation33_v1_20261011.py';s=source.read_text(encoding='utf8')
 tree=ast.parse(s);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='cases');lines=s.splitlines(keepends=True)
 cases="""def cases():
    rows=[{'kind':'anchor183','role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for sign in (1.,-1.):
        for weight in (.000625,.0025,.01,.04,.16,.5,.75,1.):
            rows.append({'kind':'CDF','role':'flag_valid','weight':weight,'sign':sign,'protect_fraction':None})
    assert len(rows)==17;return rows

"""
 lines[node.lineno-1:node.end_lineno]=[cases];s=''.join(lines)
 s=s.replace('StockRank60EmbeddingSmall512_after183_direct_allocation33_screen','StockRank60FlagOnly_after183_direct17_screen').replace('actual_StockRank60EmbeddingSmall512_after183_direct_allocation33_screen_location','actual_StockRank60FlagOnly_after183_direct17_screen_location')
 s=s.replace("    closed('actual_stock_rank60_embedding_after175_large_allocation29_screen_v1_20261011')","    closed('actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011')")
 for old,new in [(33,17),(32,16),(96,48)]:s=re.sub(r'(?<!\d)'+str(old)+r'(?!\d)',str(new),s)
 s=s.replace('return1d33','flag17').replace('passed33_own_stock_embedding_one_day_return','passed17_existing_stock_rank60_flag_only').replace("A/'stock_rank60_after183_direct33_predeclared_sources_v1_20261011.json'","A/'rank60_flag17_raw_sources_predeclared_v1_20261011.json'")
 raw=save(A/'run_rank60_flag17_after183_direct17_v1_20261011.py',s)
 names=['verify_stock_rank60medium_best33_native14_v2_20261011.py','prepare_StockRank60MediumBest33Early_selected_candidate_v2_20261011.py','run_StockRank60MediumBest33Early_selected_candidate_feature_cache_v2_20261011.py','seal_StockRank60MediumBest33Early_selected_candidate_v2_20261011.py','seal_StockRank60MediumBest33Early_selected_candidate_v3_20261011.py','stock_rank60medium_best33_early_storage_v2_20261011.py','rank60medium2048_early_candidate_recipes_v1_20261011.py','run_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011.py','publish_actual_rank60medium2048_best33_complete_candidate_main_v1_20261011.py','prepare_verified_rank60medium2048_best33_alternate_submission_delivery_v1_20261011.py']
 outputs=[]
 for name in names:
  text=changed((A/name).read_text(encoding='utf8'));outputs.append(save(A/changed(name),text))
 pins={str(p):sha(p) for p in [Path(__file__),source,raw,*[A/n for n in names],*outputs,A/'stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json',A/'actual_StockRank60EmbeddingSmall512_full5_independent_location_v1_20261011.json']}
 protocol=A/'rank60_flag17_raw_sources_predeclared_v1_20261011.json';create(protocol,{'status':'predeclared_new_flag_only17_existing_complete_H60_bank_no_training_or_scoring_claim','input_sha256':pins,'expected_official_records':17,'expected_full_controls':16,'expected_prefix_controls':48,'parent_round':183,'selection_target':'original_official_all8_metrics_and_S','flag_only_Top_and_turnover_exclusion_is_hypothesis_not_extra_gate':True,'test_labels_read':False,'new_fits':0,'new_scores':0})
 proof=A/'rank60_flag17_best17_full_candidate_sources_admission_v1_20261011.json';create(proof,{'status':'predeclared_flag17_full36_native14_cold14_prefit7_reload_independent_cold80_gain_only','input_sha256':{**pins,str(protocol):sha(protocol)},'expected_source_score_records':17,'expected_native_cases':14,'expected_cold_cases':14,'expected_prefit_refusals':7,'maximum_new_models':1,'candidate_dispatch_only_if_strictly_higher_official_TRAIN_S':True,'test_labels_read':False,'new_fits':0,'new_scores':0})
 imported=[]
 for q in outputs[:9]:importlib.import_module(q.stem);imported.append(q.name)
 create(A/'rank60_flag17_actual_runtime_import_admission_v1_20261011.json',{'status':'passed_actual9_flag17_complete_candidate_modules_imported_no_science_claim','modules':imported,'input_sha256':{str(proof):sha(proof),str(Path(__file__)):sha(__file__)},'new_fits':0,'new_scores':0})
 for name,p in [('actual_stock_rank60_flag17_after183_direct17_v1_20261011',raw),('actual_rank60_flag17_gain_selected_full_candidate_queue_v1_20261011',outputs[7]),('actual_rank60_flag17_best17_complete_candidate_main_v1_20261011',outputs[8]),('actual_verified_rank60_flag17_best17_alternate_delivery_v1_20261011',outputs[9])]:
  assert allowed();i=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),i)
 print('Flag-only17 hypothesis and complete36 candidate pipeline frozen; no new fits; scoring awaits medium60 gain handling',flush=True)

if __name__=='__main__':main()
