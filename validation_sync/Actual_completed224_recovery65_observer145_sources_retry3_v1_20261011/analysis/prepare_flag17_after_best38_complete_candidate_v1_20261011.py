"""Preserve the actual strongest37-model parent before a gain-only flag stage; no new weights."""
from pathlib import Path
import sys,ast,re,importlib
from types import SimpleNamespace
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def changed(s):
 for old,new in [('rank60_flag17','rank60_flag17_after_best38'),('StockRank60FlagOnlyBest17Early','StockRank60FlagOnlyAfterBest38Early'),('股票60日涨停股最佳17项','股票60日涨停股叠加best38最佳17项'),('60日涨停股最佳17项','60日涨停股叠加best38最佳17项'),('StockRank60EmbeddingSmall512_after183_direct_allocation17_screen','StockRank60FlagOnly_after_verified_best38_direct17_screen'),('actual_stock_rank60_embedding_after183_direct_allocation17','actual_flag17_after_verified_best38_direct17'),('rank_MLP2048_StockRank60Medium','rank_MLP512_StockRank60FlagOnly'),('predict_stock_rank60_embedding_complete_qualified_parent_scheme_v2_20261011','predict_rank60_flag17_after_best38_complete_parent_v1_20261011')]:s=s.replace(old,new)
 return s.replace('kernel16','kernel32')

def save(p,s):
 ast.parse(s);assert not p.exists(),p;p.write_text(s,encoding='utf8',newline='\n');return p

def main():
 assert allowed()
 parent_candidate=A.parent/'candidates/Rank120Rank60BestBlend38Early_v1_20261011'
 parent_release=A/'Rank120Rank60BestBlend38Early_selected_release_v1_20261011'
 prediction=read(parent_candidate/'verification.json');assert prediction['status']=='passed' and len(prediction['models'])==37
 source=A/'predict_stock_rank60_embedding_complete_qualified_parent_scheme_v2_20261011.py';text=source.read_text(encoding='utf8')
 begin=text.index('def parent_filename(');end=text.index('\n\ndef prepared_parent',begin)
 text=text[:begin]+'''def parent_filename(graph):
    from rank120_rank60_protected_after_qualified183_native_stage_v1_20261011 import GRAPH_KEY as parent_key
    assert parent_key in graph and graph[parent_key]['original_complete_parent_round']==183
    return 'predict_rank120_rank60_protected_complete_qualified183_scheme_v1_20261011.py'
'''+text[end:]
 begin=text.index('def prepared_parent(');end=text.index('\n\ndef predict(',begin)
 text=text[:begin]+'''def prepared_parent(text):
    needle='\\n        value,report=stage.after_parent(ns,context,parent,spec,component);calls.append(report);return value'
    assert text.count(needle)==1
    return text.replace(needle,needle.replace('return value','return STOCK_RANK10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT(context,value)'))
'''+text[end:]
 predictor=save(A/'predict_rank60_flag17_after_best38_complete_parent_v1_20261011.py',text)
 m=importlib.import_module(predictor.stem);assert m.parent_filename(prediction['whole_scheme_graph'])=='predict_rank120_rank60_protected_complete_qualified183_scheme_v1_20261011.py'
 mixed=A/m.parent_filename(prediction['whole_scheme_graph']);patched=m.prepared_parent(mixed.read_text(encoding='utf8'))
 # Execute the actual extracted original nested callback: complete mixed parent first, new flag callback last.
 tree=ast.parse(patched);fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='after_whole')
 calls=[];order=[]
 def joint(*args):order.append('complete_existing_mixed_parent');return args[2]+3,{'actual_fixture':True}
 def flag(context,value):order.append('new_flag_stage_after_entire_parent');return value+7
 ns={'stage':SimpleNamespace(after_parent=joint),'ns':None,'spec':None,'component':None,'calls':calls,'STOCK_RANK10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT':flag}
 exec(compile(ast.Module(body=[fn],type_ignores=[]),str(mixed),'exec'),ns)
 assert ns['after_whole'](None,11)==21 and order==['complete_existing_mixed_parent','new_flag_stage_after_entire_parent'] and len(calls)==1
 names=['verify_stock_rank60_flag17_native14_v2_20261011.py','prepare_StockRank60FlagOnlyBest17Early_selected_candidate_v2_20261011.py','run_StockRank60FlagOnlyBest17Early_selected_candidate_feature_cache_v2_20261011.py','seal_StockRank60FlagOnlyBest17Early_selected_candidate_v2_20261011.py','seal_StockRank60FlagOnlyBest17Early_selected_candidate_v3_20261011.py','stock_rank60_flag17_early_storage_v2_20261011.py','rank60_flag17_early_candidate_recipes_v1_20261011.py','run_rank60_flag17_gain_selected_full_candidate_queue_v1_20261011.py','publish_actual_rank60_flag17_best17_complete_candidate_main_v1_20261011.py','prepare_verified_rank60_flag17_best17_alternate_submission_delivery_v1_20261011.py']
 outputs=[]
 for name in names:
  s=changed((A/name).read_text(encoding='utf8'))
  if name.startswith('prepare_Stock'):
   old="    parent_candidate=ROOT/f'candidates/optimization_20261003_r{parent_number}'\n    parent_release=A/f'optimization_20261003_r{parent_number}'";assert s.count(old)==1
   s=s.replace(old,"    parent_candidate=ROOT/'candidates/Rank120Rank60BestBlend38Early_v1_20261011'\n    parent_release=A/'Rank120Rank60BestBlend38Early_selected_release_v1_20261011'")
   old="    assert read(parent_release/'full_registration_execution.json')['status']=='passed'";assert s.count(old)==1
   s=s.replace(old,"    actual_parent=read(parent_release/'selected_candidate_ready_for_registration.json');assert actual_parent['sealed_candidate_complete'] and actual_parent['new_inference_claimed'] and actual_parent['actual_saved_native_models']==37\n    receipt=read(A/'Actual_protected60_120_best_blend38_complete_candidate_sources_and_submission_main_receipt_v1_20261011.json');assert receipt['status']=='pushed_and_remote_head_verified'")
   s=s.replace("parent_release/'full_registration_execution.json'","parent_release/'selected_candidate_ready_for_registration.json'")
  if name.startswith(('publish_','prepare_verified_')):
   s=re.sub(r'(?<![A-Za-z0-9_])36(?![A-Za-z0-9_])','37',s).replace('complete36','complete37')
  outputs.append(save(A/changed(name),s))
 proof=A/'rank60_flag17_after_best38_best17_full_candidate_sources_admission_v1_20261011.json'
 paths=[Path(__file__),source,predictor,mixed,*[A/n for n in names],*outputs,parent_candidate/'manifest.json',parent_candidate/'verification.json',parent_release/'selected_candidate_ready_for_registration.json',A/'flag17_after_verified_best38_raw_sources_admission_v1_20261011.json']
 create(proof,{'status':'passed_actual_original_mixed_parent_callback_then_flag_stage_CPU_execution_and_complete37_gain_only_candidate_predeclaration','input_sha256':{str(p):sha(p) for p in paths},'actual_callback_order':order,'actual_parent_models':37,'additional_unique_models_expected':0,'expected_source_score_records':17,'expected_native_cases':14,'expected_cold_cases':14,'expected_prefit_refusals':7,'full_independent_two_replays_and_cold80_required':True,'parent_full_connected_board_pending_honestly_retained':True,'new_fits':0,'new_scores':0,'test_labels_read':False})
 imported=[]
 for q in outputs[:9]:importlib.import_module(q.stem);imported.append(q.name)
 create(A/'flag17_after_best38_actual_callback_and9_runtime_imports_admission_v1_20261011.json',{'status':'passed_actual_mixed_parent_AST_callback_execution_order_and9_runtime_imports','input_sha256':{str(proof):sha(proof),str(Path(__file__)):sha(__file__)},'modules':imported,'new_fits':0,'new_scores':0})
 for name,p in [('actual_rank60_flag17_after_best38_gain_selected_full_candidate_queue_v1_20261011',outputs[7]),('actual_rank60_flag17_after_best38_best17_complete_candidate_main_v1_20261011',outputs[8]),('actual_verified_rank60_flag17_after_best38_best17_alternate_delivery_v1_20261011',outputs[9])]:
  assert allowed();i=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),i)
 print('Actual complete mixed parent before new flag callback verified; all37 reload/independent/cold80 candidate path and main/delivery queued only on real S gain',flush=True)

if __name__=='__main__':main()
