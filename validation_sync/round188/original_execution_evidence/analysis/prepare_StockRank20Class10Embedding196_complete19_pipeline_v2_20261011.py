"""Freeze fresh weighted-loss family routes; reuse completed scores without new fits."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
import prepare_StockRank10Embedding192_complete48_pipeline_v2_20261011 as previous

FACTORY=Path(__file__).stem
PROOF='stock_rank20class10_embedding196_full_execution_sources_admission_v1_20261011.json'
def basic(s):
 s=s.replace('StockRank10','StockRank20Class10').replace('stock_rank10','stock_rank20class10').replace('STOCK_RANK10','STOCK_RANK20CLASS10').replace('rank10mean','rank20mean').replace('Rank10Mean','Rank20MeanTail4')
 s=s.replace('17801','17967').replace('qa103','qa107').replace('QA103','QA107').replace('qa_v103','qa_v107')
 s=re.sub(r'(?<!\d)48(?!\d)','19',s)
 s=s.replace('(19,44,132)','(19,16,48)').replace('(44,132)','(16,48)').replace("'actual_nonidentity_full_controls':44","'actual_nonidentity_full_controls':16").replace("'actual_nonidentity_prefix_controls':132","'actual_nonidentity_prefix_controls':48").replace("anchor_round'] in (175,","anchor_round'] in (183,")
 return re.sub(r'(?<!\d)(192|191|475|103)(?!\d)',lambda m:{'192':'196','191':'195','475':'479','103':'107'}[m.group()],s)
NAMES=[basic(n) for n in previous.NAMES]
EXTRAS=[basic(n) for n in previous.EXTRAS[:18]]+['rank20class10_complete19_normalization_native14_sources_admission_v1_20261011.json','stock_rank20class10_embedding195_full_execution_sources_admission_v1_20261011.json',*previous.EXTRAS[-2:]]
def source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS]]))

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
 aliases.update({'recovery16_MixedRefined191_complete27_family_v1_20261011':'StockRank20Class10Embedding195_complete48_family_v1_20261011',
 'actual_stock_rank10_embedding_own_training_and_full5_queue_v2_20261011':'actual_stock_rank20class10_BCE_own6_full5_queue_v1_20261011'})
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(aliases,key=len,reverse=True)))
 for p in inputs:
  text=basic(pattern.sub(lambda m:aliases[m.group()],p.read_text(encoding='utf8')))
  text=text.replace('from owned_idle_publication_wait_runtime_v1_20261010 import hold','from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold').replace('from publish_explicit_parent_training_round_v2_20261005 import publish','from publish_explicit_parent_training_round_external_frozen_v3_20261011 import publish')
  # Screen folders are actual October11 outputs, unlike the legacy template suffix.
  if p.name==previous.EXTRAS[0]:text=text.replace("family['name']+'_screen_v1_20261010'","family['name']+'_screen_v1_20261011'")
  outputs.append(save(A/basic(p.name),text))
 plan=read(A/previous.EXTRAS[11]);plan.update(status='predeclared19_new_rank20_tail4_weighted_loss_and175193_qualified_anchors_before_scoring',fully_qualified_anchors=[183,195],label_horizon_trading_days=20,loss_weighting='balanced_mature_rank20_top10_binary')
 plan.update(status='predeclared19_actual_latest183_Top10_BCE17_and183195_complete_anchors_before_scores',expected_records=19,fully_qualified_anchors=[183,195],families=[{'name': 'StockRank20Class10EmbeddingSmall512_after183_high_impact17', 'actual_service': 'actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011', 'records': 17, 'base_round': 183, 'stage_kind': 'stock_rank20class10_embedding_rank20mean_direct', 'main_receipt': 'Class10_after183_actual17_sources_main_receipt_v1_20261011.json'}])
 if (A/EXTRAS[11]).exists():assert read(A/EXTRAS[11])==plan
 else:create(A/EXTRAS[11],plan)
 for n in [EXTRAS[12],EXTRAS[13],*EXTRAS[14:18]]:assert (A/n).is_file(),n
 stage=importlib.import_module(Path(EXTRAS[14]).stem)
 normal=importlib.import_module(Path(EXTRAS[0]).stem)
 assert set(normal.RECIPES)==set(stage.BACKENDS)
 native=importlib.import_module(Path(EXTRAS[15]).stem)
 assert native.CONFIG['epochs']==64 and native.CONFIG['training_calendar_window']==252
 assert native.CONFIG['loss_weighting']=='balanced_mature_rank20_top10_binary'
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(196,195,(479,))
 assert '(196, 107, 19)' in (A/NAMES[-1]).read_text(encoding='utf8')
 candidate=(A/EXTRAS[3]).read_text(encoding='utf8')
 assert 'pilot19.json' in candidate
 assert {v[1] for v in normal.RECIPES.values()}=={'stock_rank20class10_embedding_small512_BF16_bank6_v1_20261011'}
 for p in outputs:
  for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
   if isinstance(node,ast.ImportFrom) and node.module and ('StockRank20Class10' in node.module or 'stock_rank20class10' in node.module):assert (A/(node.module+'.py')).is_file(),(p.name,node.module)
 storage=importlib.import_module(Path(EXTRAS[2]).stem);assert len(storage.OUTPUTS)==6
 assert all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,*[A/n for n in EXTRAS[11:18]],A/EXTRAS[19]]}
 for n in EXTRAS[9:11]:create(A/n,{'status':'compiled_fresh196_exact19_QA107_W479_own_tail4_sources_before_future','input_sha256':pins,'new_fits':0,'new_scores':0,'actual_future_X_read':False})
 create(A/EXTRAS[18],{'status':'compiled19_actual_score_rehash_and_native14_routes_before_completed_tail4_scores','input_sha256':pins,'expected_records':19,'expected_full_controls':16,'expected_prefix_controls':48,'anchor_rounds':[175,195],'new_fits':0,'new_scores':0})
 create(A/PROOF,{'status':'compiled196_exact19_QA107_17967_W479_weighted_Huber_tail4_before_future','input_sha256':pins,'expected_records':19,'expected_board':17967,'actual_callback_CPU_count':11,'new_fits':0,'new_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 assert all(p.is_file() for p in source_paths())
 # Canonical terminal helper recognizes completed owned workers without waiting for parent cleanup.
 tasks=[('actual_stock_rank20class10_embedding19_after195_normalization_queue_v1_20261011',EXTRAS[0]),('StockRank20Class10Embedding19_selected_native14_v1_20261011',EXTRAS[1])]
 for name,driver in tasks:
  p=A/(Path(driver).stem+'_canonical_terminal_wrapper_v1_20261011.py')
  save(p,"from pathlib import Path\nimport sys,importlib\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed\nif __name__=='__main__':\n assert allowed();m=importlib.import_module("+repr(Path(driver).stem)+");m.closed=closed;m.main()\n")
  assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),row)
 name='StockRank20Class10Embedding196_complete19_family_v1_20261011';driver=EXTRAS[5]
 assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),row)
 print({'196_complete19_routes_queued':True,'new_fits':0,'new_scores':0,'submission_qualification_pending':True},flush=True)
if __name__=='__main__':main()
