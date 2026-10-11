"""Freeze complete200: actual pureH60 direct33 plus complete183 and199 anchors."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
import prepare_StockRank20Class10Embedding196_complete19_pipeline_v2_20261011 as template
FACTORY=Path(__file__).stem
PROOF='stock_rank60_direct200_complete35_sources_admission_v5_20261011.json'

def basic(s):
 for old,new in [('StockRank20Class10','StockRank60Direct'),('stock_rank20class10','stock_rank60_direct'),('STOCK_RANK20CLASS10','STOCK_RANK60_DIRECT'),('Rank20MeanTail4','Rank60Mean'),('rank20mean','rank60mean'),('qa_v107','qa_v111'),('qa107','qa111'),('QA107','QA111'),('17967','18149')]:s=s.replace(old,new)
 s=re.sub(r'(?<!\d)(196|195|479|107)(?!\d)',lambda m:{'196':'200','195':'199','479':'483','107':'111'}[m.group()],s)
 # Counts embedded in artifact names and status text must agree with the new plan.
 s=s.replace('complete19','complete35').replace('embedding19','embedding35').replace('Embedding19','Embedding35').replace('pilot19','pilot35').replace('full19','full35').replace('actual19','actual35').replace('normalized19','normalized35').replace('anchor19','anchor35').replace('records19','records35')
 s=re.sub(r'(?<!\d)19(?!\d)','35',s)
 s=s.replace('(35,16,48)','(35,32,96)').replace('(16,48)','(32,96)').replace('(16, 48)','(32, 96)').replace("'actual_nonidentity_full_controls':16","'actual_nonidentity_full_controls':32").replace("'actual_nonidentity_prefix_controls':48","'actual_nonidentity_prefix_controls':96")
 s=s.replace('stock_rank60_direct_embedding16_','stock_rank60_embedding16_').replace('stock_rank60_direct_embedding_rank60mean_direct','stock_rank60_embedding_rank60mean_direct').replace("GRAPH_KEY='stock_rank60_direct_embedding_after_complete_qualified_parent_v1_20261011'","GRAPH_KEY='stock_rank60_embedding_after_complete_qualified_parent_v1_20261011'")
 return s

def artifact(n):
 s=basic(n)
 return re.sub(r'_v\d+_20261011','_v5_20261011',s)
NAMES=[artifact(n) for n in template.NAMES]
EXTRAS=[artifact(n) for n in template.EXTRAS[:12]]+[
 'predict_stock_rank60_embedding_complete_qualified_parent_scheme_v2_20261011.py',
 'stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json',
 'stock_rank60_embedding_after_complete_qualified_parent_native_stage_v2_20261011.py',
 'stock_rank60_embedding_small512_BF16_native_v1_20261011.py',
 'stock_rank60_embedding_saved_tensor_decoder_v1_20261011.py',
 'stock_rank60_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json',
 'stock_rank60_direct35_normalization_native14_sources_admission_v5_20261011.json',
 'rank60_rank20_mixed199_full_execution_sources_admission_v1_20261011.json',
 'exact_verified_feature120_memoization_runtime_v1_20261010.py',
 'actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json',
 'stock_rank60_after183_direct33_predeclared_sources_v1_20261011.json',
 'actual_latest183_parent196198_routes37_v1_20261011.json',
 'verified_shared_publication_board_loader_v1_20261011.py',
 'late_bound_shared_snapshot_encoder_runtime_v1_20261011.py',
 'verified_shared_publication_board_loader_actual_complete180_controls_v1_20261011.json']
def source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS]]))
def save(p,s):
 assert not p.exists(),p;ast.parse(s);p.write_text(s,encoding='utf8');return p

def main():
 assert allowed()
 routes=read(A/'actual_latest183_parent196198_routes37_v1_20261011.json')
 actual=routes['actual_source_overrides']
 overrides={**actual,template.EXTRAS[0]:'normalize_completed_stock_rank20class10_embedding_complete19_after195_exact_v4_20261011.py',template.EXTRAS[1]:'qualify_stock_rank20class10_embedding19_selected_native14_v2_20261011.py'}
 originals=template.NAMES+template.EXTRAS[:9]
 aliases=dict(zip(template.NAMES+template.EXTRAS[:12],NAMES+EXTRAS[:12]))
 aliases.update(dict(zip(template.EXTRAS[12:18],EXTRAS[12:18])))
 aliases.update({'prepare_StockRank20Class10Embedding196_complete19_pipeline_v2_20261011.py':FACTORY+'.py',
 'stock_rank20class10_embedding_after_complete_qualified_parent_native_stage_v2_20261011.py':EXTRAS[14],
 'predict_stock_rank20class10_embedding_complete_qualified_parent_scheme_v2_20261011.py':EXTRAS[12],
 'stock_rank20class10_actual_twelve_parent_callbacks_CPU_controls_v2_20261011.json':EXTRAS[13],
 'stock_rank20class10_embedding195_full_execution_sources_admission_v1_20261011.json':EXTRAS[19]})
 for old,new in list(aliases.items()):
  if old in overrides:aliases[overrides[old]]=new
 aliases.update({Path(k).stem:Path(v).stem for k,v in list(aliases.items()) if k.endswith('.py')})
 # Only idle administrative dependency identities change; the real original score/native workers stay intact.
 for old in ('StockRank20Class10Embedding195_complete48_family_v1_20261011','StockRank20Class10Embedding195_complete19_family_v1_20261011','recovery36_StockRank20Class10Embedding195_complete48_family_v1_20261011'):
  aliases[old]='Rank60Rank20Mixed199_complete51_family_v4_20261011'
 aliases['actual_stock_rank20class10_BCE_own6_full5_queue_v1_20261011']='actual_stock_rank60_mature_objective_own6_full5_queue_v1_20261011'
 aliases['recovery37_StockRank20Class10Embedding196_selected_candidate_preparation_v1_20261011']='StockRank60DirectEmbedding200_selected_candidate_preparation_v5_20261011'
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(aliases,key=len,reverse=True)))
 outputs=[];inputs=[]
 for old in originals:
  p=A/overrides.get(old,old);inputs.append(p)
  s=basic(pattern.sub(lambda m:aliases[m.group()],p.read_text(encoding='utf8')))
  s=s.replace('from owned_idle_publication_wait_runtime_v1_20261010 import hold','from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold').replace('from publish_explicit_parent_training_round_v2_20261005 import publish','from publish_explicit_parent_training_round_external_frozen_v3_20261011 import publish')
  s=s.replace('qualified175','qualified183').replace('actual_stock_rank60_direct_BCE_own6_full5_queue_v1_20261011','actual_stock_rank60_mature_objective_own6_full5_queue_v1_20261011')
  # Use the canonical versioned200 service identities which this family actually launches.
  for suffix in ('selected_candidate_preparation','selected_candidate_sealing','round200_full_registration'):
   s=s.replace('StockRank60DirectEmbedding200_'+suffix+'_v1_20261011','StockRank60DirectEmbedding200_'+suffix+'_v5_20261011')
  if old==template.EXTRAS[5]:
   s=s.replace('from handoff_ready_goss_full_execution_20261006 import start_service','from start_fast_completed_owned_service_v1_20261011 import start_service')
  outputs.append(save(A/aliases[old],s))
 plan=read(A/template.EXTRAS[11])
 plan.update(status='predeclared35_pure_mature60_direct33_after183_and_complete183199_anchors',expected_records=35,fully_qualified_anchors=[183,199],label_horizon_trading_days=60,loss_weighting='mature_rank60_Huber',families=[{'name':'StockRank60EmbeddingSmall512_after183_direct_allocation33','actual_service':'actual_stock_rank60_embedding_after183_direct_allocation33_v1_20261011','records':33,'base_round':183,'stage_kind':'stock_rank60_embedding_rank60mean_direct','main_receipt':'Rank60_after183_actual33_sources_main_receipt_v1_20261011.json'}])
 create(A/EXTRAS[11],plan)
 # Validate the actual generated count, anchor loop, imports and available immutable E storage.
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(200,199,(483,))
 assert '(200, 111, 35)' in (A/NAMES[-1]).read_text(encoding='utf8')
 normal=(A/EXTRAS[0]).read_text(encoding='utf8');assert 'for number in (183,199):' in normal and '(35,32,96)' in normal
 assert "'stock_rank60_embedding16_cross120_rank60mean_recent252_small512_BF16_e64'" in normal
 candidate=(A/EXTRAS[3]).read_text(encoding='utf8');assert 'parent_number in (183,199)' in candidate
 for p in outputs:
  for n in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
   if isinstance(n,ast.ImportFrom) and n.module and ('StockRank60Direct' in n.module or 'stock_rank60_direct' in n.module):assert (A/(n.module+'.py')).is_file(),(p,n.module)
 stage=importlib.import_module(Path(EXTRAS[14]).stem);norm=importlib.import_module(Path(EXTRAS[0]).stem);assert set(norm.RECIPES)==set(stage.BACKENDS)
 storage=importlib.import_module(Path(EXTRAS[2]).stem);assert len(storage.OUTPUTS)==6 and all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
 assert "service_owned_workflows_20261006/StockRank60DirectEmbedding200_selected_candidate_preparation_v5_20261011" in (A/EXTRAS[4]).read_text(encoding='utf8')
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/EXTRAS[11],*[A/n for n in EXTRAS[12:18]],*[A/n for n in EXTRAS[19:]]]}
 for n in [EXTRAS[9],EXTRAS[10],EXTRAS[18]]:create(A/n,{'status':'compiled200_complete35_QA111_18149_W483_before_selected_native14_and_future','input_sha256':pins,'expected_records':35,'actual_future_X_read':False,'new_fits':0,'new_scores':0})
 create(A/PROOF,{'status':'compiled200_complete35_QA111_18149_W483_corrected183_callbacks_before_future','input_sha256':pins,'expected_records':35,'expected_board':18149,'expected_CPU_callbacks':12,'new_fits':0,'new_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 assert all(p.is_file() for p in source_paths())
 for name,driver in [('actual_stock_rank60_direct35_after199_normalization_v5_20261011',EXTRAS[0]),('StockRank60DirectEmbedding35_selected_native14_v1_20261011',EXTRAS[1]),('StockRank60DirectEmbedding200_complete35_family_v5_20261011',EXTRAS[5])]:
  assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(A/PROOF):sha(A/PROOF)})
  create(A/(name+'_activation.json'),row)
 print({'complete200_35_sources_compiled_and_queued':True,'new_fits_or_scores':0,'qualification_pending':True},flush=True)
if __name__=='__main__':main()
