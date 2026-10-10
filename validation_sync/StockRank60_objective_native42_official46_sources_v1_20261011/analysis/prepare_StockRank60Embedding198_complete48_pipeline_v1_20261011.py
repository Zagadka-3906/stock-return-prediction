"""Freeze fresh weighted-loss family routes; reuse completed scores without new fits."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
import prepare_StockRank10Embedding192_complete48_pipeline_v2_20261011 as previous

FACTORY=Path(__file__).stem
PROOF='stock_rank60_embedding198_full_execution_sources_admission_v1_20261011.json'
def basic(s):
 s=s.replace('StockRank10','StockRank60').replace('stock_rank10','stock_rank60').replace('STOCK_RANK10','STOCK_RANK60').replace('rank10mean','rank60mean').replace('Rank10Mean','Rank60Mean')
 s=s.replace('17801','18063').replace('qa103','qa109').replace('QA103','QA109').replace('qa_v103','qa_v109')
 return re.sub(r'(?<!\d)(192|191|475|103)(?!\d)',lambda m:{'192':'198','191':'197','475':'481','103':'109'}[m.group()],s)
NAMES=[basic(n) for n in previous.NAMES]
EXTRAS=[basic(n) for n in previous.EXTRAS[:18]]+['rank60_complete48_normalization_native14_sources_admission_v1_20261011.json','stock_rank20class25_embedding197_full_execution_sources_admission_v1_20261011.json',*previous.EXTRAS[-2:]]
def source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS],A/'verified_shared_publication_board_loader_v1_20261011.py',A/'late_bound_shared_snapshot_encoder_runtime_v1_20261011.py',A/'verified_shared_publication_board_loader_actual_complete180_controls_v1_20261011.json',A/'unified_completed_parent_shared_publication36_routes_v1_20261011.json']))

def save(p,s):
 if p.exists():
  assert p.read_text(encoding='utf8')==s,p
  return p
 if p.suffix=='.py':compile(s,str(p),'exec')
 p.write_text(s,encoding='utf8',newline='\n');return p

def main():
 assert allowed();outputs=[];inputs=[A/n for n in previous.NAMES+previous.EXTRAS[:9]]
 aliases={n:basic(n) for n in previous.NAMES+previous.EXTRAS[:18]}
 aliases['prepare_StockRank10Embedding192_complete48_pipeline_v2_20261011.py']=FACTORY+'.py'
 aliases['prepare_StockRank10Embedding192_complete48_pipeline_v2_20261011']=FACTORY
 aliases.update({Path(k).stem:Path(v).stem for k,v in list(aliases.items()) if k.endswith('.py')})
 aliases.update({'recovery16_MixedRefined191_complete27_family_v1_20261011':'StockRank20Class25Embedding197_complete48_family_v1_20261011',
 'actual_stock_rank10_embedding_own_training_and_full5_queue_v2_20261011':'actual_stock_rank60_mature_objective_own6_full5_queue_v1_20261011'})
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(aliases,key=len,reverse=True)))
 for p in inputs:
  text=basic(pattern.sub(lambda m:aliases[m.group()],p.read_text(encoding='utf8')))
  text=text.replace('from late_bound_snapshot_encoder_runtime_v1_20261010 import installed','from late_bound_shared_snapshot_encoder_runtime_v1_20261011 import installed')
  text=text.replace('from owned_idle_publication_wait_runtime_v1_20261010 import hold','from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold').replace('from publish_explicit_parent_training_round_v2_20261005 import publish','from publish_explicit_parent_training_round_external_frozen_v3_20261011 import publish')
  # Screen folders are actual October11 outputs, unlike the legacy template suffix.
  if p.name==previous.EXTRAS[0]:text=text.replace("family['name']+'_screen_v1_20261010'","family['name']+'_screen_v1_20261011'")
  outputs.append(save(A/basic(p.name),text))
 plan=read(A/previous.EXTRAS[11]);plan.update(status='predeclared48_true60_mature_Huber_and175197_qualified_anchors_before_scoring',fully_qualified_anchors=[175,197],label_horizon_trading_days=60,loss='Huber',huber_delta=.1)
 plan['families']=[{k:basic(v) if isinstance(v,str) else v for k,v in f.items()} for f in plan['families']]
 if (A/EXTRAS[11]).exists():assert read(A/EXTRAS[11])==plan
 else:create(A/EXTRAS[11],plan)
 for n in [EXTRAS[12],EXTRAS[13],*EXTRAS[14:18]]:assert (A/n).is_file(),n
 stage=importlib.import_module(Path(EXTRAS[14]).stem)
 normal=importlib.import_module(Path(EXTRAS[0]).stem)
 assert set(normal.RECIPES)==set(stage.BACKENDS)
 native=importlib.import_module(Path(EXTRAS[15]).stem)
 assert native.CONFIG['epochs']==64 and native.CONFIG['training_calendar_window']==252
 assert native.CONFIG['loss']=='Huber' and native.CONFIG['label_horizon_trading_days']==60 and native.CONFIG['target']=='y_rank_60mean'
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(198,197,(481,))
 assert '(198, 109, 48)' in (A/NAMES[-1]).read_text(encoding='utf8')
 candidate=(A/EXTRAS[3]).read_text(encoding='utf8')
 assert 'pilot48.json' in candidate
 assert {v[1] for v in normal.RECIPES.values()}=={'stock_rank60_embedding_small512_BF16_bank6_v1_20261011'}
 for p in outputs:
  for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
   if isinstance(node,ast.ImportFrom) and node.module and ('StockRank60' in node.module or 'stock_rank60' in node.module):assert (A/(node.module+'.py')).is_file(),(p.name,node.module)
 storage=importlib.import_module(Path(EXTRAS[2]).stem);assert len(storage.OUTPUTS)==6
 assert all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,*[A/n for n in EXTRAS[11:18]],A/EXTRAS[19]]}
 for n in EXTRAS[9:11]:create(A/n,{'status':'compiled_fresh198_exact48_QA109_W481_own60_sources_before_future','input_sha256':pins,'new_fits':0,'new_scores':0,'actual_future_X_read':False})
 create(A/EXTRAS[18],{'status':'compiled48_actual_score_rehash_and_native14_routes_before_completed_rank60_scores','input_sha256':pins,'expected_records':48,'expected_full_controls':44,'expected_prefix_controls':132,'anchor_rounds':[175,197],'new_fits':0,'new_scores':0})
 create(A/PROOF,{'status':'compiled198_exact48_QA109_18063_W481_true60_mature_Huber_before_future','input_sha256':pins,'expected_records':48,'expected_board':18063,'actual_callback_CPU_count':11,'new_fits':0,'new_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 assert all(p.is_file() for p in source_paths())
 # Canonical terminal helper recognizes completed owned workers without waiting for parent cleanup.
 tasks=[('actual_stock_rank60_embedding48_after197_normalization_queue_v1_20261011',EXTRAS[0]),('StockRank60Embedding48_selected_native14_v1_20261011',EXTRAS[1])]
 for name,driver in tasks:
  p=A/(Path(driver).stem+'_canonical_terminal_wrapper_v1_20261011.py')
  save(p,"from pathlib import Path\nimport sys,importlib\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed\nif __name__=='__main__':\n assert allowed();import route_unified_completed_parent_shared_publication36_v1_20261011 as routes;closed,_,_=routes.installed();m=importlib.import_module("+repr(Path(driver).stem)+");m.closed=closed;m.main()\n")
  assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),row)
 p=save(A/'alias_actual_rank60_official46_completed_main_receipt_v1_20261011.py',"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom run_dependency_queue_v3_20261006 import read,sha,create\nfrom prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed\nif __name__=='__main__':\n assert allowed();closed('actual_stock_rank60_objective_stages_main_v1_20261011')\n p=A/'StockRank60_objective_native42_official46_sources_main_receipt_v1_20261011.json';r=read(p);assert r['status']=='pushed_and_remote_head_verified' and r['branch']=='main'\n create(A/'StockRank60_objective_native42_official46_main_receipt_v1_20261011.json',{**r,'actual_receipt_source':str(p),'actual_receipt_sha256':sha(p),'new_scores':0})\n")
 family=A/'run_StockRank60Embedding198_complete_family_current36_wrapper_v1_20261011.py'
 save(family,"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_unified_completed_parent_shared_publication36_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(EXTRAS[5])+")\n")
 for name,driver in [('actual_rank60_official46_main_receipt_alias_v1_20261011',p.name),('StockRank60Embedding198_complete48_family_v1_20261011',family.name)]:
  assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),row)
 print({'198_complete48_routes_queued':True,'new_fits':0,'new_scores':0,'submission_qualification_pending':True},flush=True)
if __name__=='__main__':main()
