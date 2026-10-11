from pathlib import Path
import sys,importlib,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
def main():
 assert allowed();overrides={};corrections=[]
 changes={'run_rank10_rank20_after175_higher_allocation49_screen_v1_20261011.py':[("right['configuration']['label_horizon_trading_days']==5","right['configuration']['label_horizon_trading_days']==10"),("right['configuration']['target']=='y_rank_5mean'","right['configuration']['target']=='y_rank_10mean'")],
 'normalize_completed_stock_rank10_embedding_complete48_after191_v1_20261011.py':[("family['name']+'_screen_v1_20261010'","family['name']+'_screen_v1_20261011'")]}
 for n,edits in changes.items():
  p=A/n;q=A/n.replace('_v1_20261011','_exact_recovery17_v2_20261011');assert not q.exists();s=p.read_text(encoding='utf8')
  for old,new in edits:assert s.count(old)==1,(n,old);s=s.replace(old,new)
  compile(s,str(q),'exec');q.write_text(s,encoding='utf8',newline='\n');overrides[n]=q.name;corrections.append(q)
 # Failed49 stopped before frozen/scoring/output creation. No cached scores are overwritten.
 assert not Path('E:/赛题五_本机临时/StockRank10Rank20_after175_higher_allocation49_screen_v1_20261011').exists()
 base=[('actual_rank10_rank20_after175_higher_allocation49_screen_v1_20261011','run_rank10_rank20_after175_higher_allocation49_screen_v1_20261011.py'),('actual_rank10_rank20_higher49_completed_official_main_v1_20261011','publish_actual_rank10_rank20_higher49_after_complete_v1_20261011.py'),('actual_rank10_rank20_mixed_selected_native14_v1_20261011','verify_rank10_rank20_mixed_selected_native14_v1_20261011.py'),('actual_stock_rank10_embedding48_after191_normalization_queue_v1_20261011','normalize_completed_stock_rank10_embedding_complete48_after191_v1_20261011.py'),('StockRank10Embedding48_selected_native14_v1_20261011','qualify_stock_rank10_embedding48_selected_native14_v1_20261011.py'),('StockRank10Embedding192_complete48_family_v1_20261011','run_StockRank10Embedding192_complete_family_v1_20261011.py'),('actual_rank10_rank20_higher51_after192_normalization_v1_20261011','normalize_completed_rank10_rank20_higher51_after192_v1_20261011.py'),('actual_rank10_rank20_higher51_selected_native14_v1_20261011','qualify_rank10_rank20_higher51_selected_native14_v1_20261011.py'),('Rank10Rank20Higher193_complete51_family_v4_20261011','run_Rank10Rank20Higher193_complete_family_v4_20261011.py'),('actual_stock_rank20tail4_embedding48_after193_normalization_queue_v1_20261011','normalize_completed_stock_rank20tail4_embedding_complete48_after193_v1_20261011.py'),('StockRank20Tail4Embedding48_selected_native14_v1_20261011','qualify_stock_rank20tail4_embedding48_selected_native14_v1_20261011.py'),('StockRank20Tail4Embedding194_complete48_family_v1_20261011','run_StockRank20Tail4Embedding194_complete_family_v1_20261011.py')]
 factories=['prepare_StockRank10Embedding192_complete48_pipeline_v2_20261011','prepare_Rank10Rank20Higher193_complete51_pipeline_v4_20261011','prepare_StockRank20Tail4Embedding194_complete48_pipeline_v1_20261011']
 drivers={d for n,d in base};aliases={n:'recovery17_'+n for n,d in base}
 for f in factories:
  m=importlib.import_module(f);drivers.update(m.EXTRAS[:9])
  for n in m.EXTRAS[3:9]:
   s=(A/n).read_text(encoding='utf8')
   import ast
   for node in ast.walk(ast.parse(s)):
    if isinstance(node,ast.Constant) and isinstance(node.value,str) and ('192' in node.value or '193' in node.value or '194' in node.value) and ('selected_candidate_preparation' in node.value or 'selected_candidate_sealing' in node.value or 'full_registration' in node.value) and not node.value.endswith(('.json','.py')) and '/' not in node.value and '\\' not in node.value:aliases[node.value]='recovery17_'+node.value
 wrappers={};wrapperfiles=[]
 for d in sorted(drivers):
  assert (A/d).is_file(),d
  p=A/(Path(d).stem+'_new_objectives_recovery17_wrapper.py');assert not p.exists()
  s="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_new_objectives_exact_source_recovery17_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(d)+")\n"
  compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');wrappers[d]=p.name;wrapperfiles.append(p)
 preserved=[]
 for n,d in base:
  folder=A/'service_owned_workflows_20261006'/n
  if not (folder/'native_launch.json').exists():continue
  row=read(folder/'native_launch.json');stack=None;terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
  if owned(row):
   p=psutil.Process(row['owned_worker_pid']);assert not p.children(),n
   stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout
   assert 'closed (' in stack,n
   retire(row,'Replace exact idle helper before scientific output dispatch, real10 horizon assertion and actual11 screen folder correction; original source/failures preserved')
  preserved.append({'name':n,'identity':row,'terminal':terminal,'actual_idle_stack':stack})
 proof=A/'new_objectives_exact_source_recovery17_routes_v1_20261011.json'
 paths=[Path(__file__),A/'route_new_objectives_exact_source_recovery17_v1_20261011.py',*corrections,*wrapperfiles,*[A/d for d in drivers],*[A/(f+'.py') for f in factories]]
 create(proof,{'status':'compiled_real_rank10_not5_assertion_and_actual11_screen_folder_before_any_new_scores','input_sha256':{str(p):sha(p) for p in paths},'source_overrides':overrides,'service_aliases':aliases,'driver_wrappers':wrappers,'source_factories':factories,'remaining_tasks':base,'preserved_prior_helpers_and_failures':preserved,'new_fits':0,'new_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 for n,d in base:
  assert allowed();p=A/wrappers[d];row=start_service(aliases[n],p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(aliases[n]+'_activation.json'),row)
 print({'recovery17_actual_dispatch':len(base),'reused_own_annual_banks':True,'new_fits':0,'new_scores':0},flush=True)
if __name__=='__main__':main()
