from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 import prepare_StockRank10Embedding192_complete48_pipeline_v2_20261011 as factory
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/factory.NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(192,191,(475,))
 assert '(192, 103, 48)' in (A/factory.NAMES[-1]).read_text(encoding='utf8')
 import stock_rank10_embedding_small512_BF16_native_v1_20261011 as native
 assert native.CONFIG['target']=='y_rank_10mean' and native.CONFIG['label_horizon_trading_days']==10 and native.CONFIG['training_calendar_window']==252 and native.CONFIG['epochs']==64
 import normalize_completed_stock_rank10_embedding_complete48_after191_v1_20261011 as normal
 import stock_rank10_embedding_after_complete_qualified_parent_native_stage_v1_20261011 as stage
 assert set(normal.RECIPES)==set(stage.BACKENDS)
 callbacks=read(A/'stock_rank10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json');assert len(callbacks['records'])==11
 rows=[]
 for name in factory.NAMES+factory.EXTRAS:
  p=A/name;assert p.is_file(),name
  if p.suffix!='.py':continue
  text=p.read_text(encoding='utf8');tree=ast.parse(text);compile(text,str(p),'exec')
  for bad in ('4660','stock_rank20long','StockRank20Long','recent504','Recent504','rank20mean','Rank20Mean','qa99','17538'):assert bad not in text,(name,bad)
  for node in ast.walk(tree):
   if isinstance(node,ast.ImportFrom) and node.module and ('192' in node.module or 'stock_rank10' in node.module):assert (A/(node.module+'.py')).is_file(),(name,node.module)
   if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.endswith('.py') and '/' not in node.value and '\\' not in node.value and ('192' in node.value or 'stock_rank10' in node.value):assert (A/node.value).is_file(),(name,node.value)
  rows.append({'source':name,'sha256':sha(p),'compiled_and_direct_new_imports_and_literals_checked':True})
 candidate=(A/'prepare_StockRank10Embedding192_selected_candidate_v1_20261011.py').read_text(encoding='utf8')
 assert '(1599600,344,4650)' in candidate
 cache=(A/'run_StockRank10Embedding192_selected_candidate_feature_cache_v1_20261011.py').read_text(encoding='utf8');assert '80*4650' in cache
 seal=(A/'seal_StockRank10Embedding192_selected_candidate_v1_20261011.py').read_text(encoding='utf8');assert 'closed(service.name)' in seal
 registry=(A/'run_StockRank10Embedding192_full_registration_v1_20261011.py').read_text(encoding='utf8');assert 'main_publisher_reboot_v12_20261011' in registry
 create(A/'stock_rank10_192_actual_materialized_source_controls_v1_20261011.json',{'status':'passed_actual_materialized_192_48_QA103_17801_W475_sources_own_horizon10_window252_and_true4650_guards','records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(factory.__file__),A/'stock_rank10_embedding192_full_execution_sources_admission_v1_20261011.json']},'new_fits':0,'new_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 print({'materialized_new_rank10_192_source_checks':len(rows),'new_scores':0},flush=True)
if __name__=='__main__':main()
