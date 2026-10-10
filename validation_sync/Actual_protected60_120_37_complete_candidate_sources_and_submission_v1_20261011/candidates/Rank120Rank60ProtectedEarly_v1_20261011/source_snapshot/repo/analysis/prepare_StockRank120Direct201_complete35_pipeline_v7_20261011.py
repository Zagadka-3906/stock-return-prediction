"""Prospective201: pure120 actual33 plus complete183/200, with every runtime wait audited."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
import prepare_StockRank60Direct200_complete35_pipeline_v6_20261011 as template
FACTORY=Path(__file__).stem
PROOF='stock_rank120_direct201_complete35_sources_admission_v7_20261011.json'
PARENT='recovery40_StockRank60DirectEmbedding200_complete35_family_v6_20261011'
def changed(s):
 s=s.replace('Rank60Rank20Mixed199_complete51_family_v4_20261011','__ACTUAL_PARENT_201__')
 for old,new in [('StockRank60Direct','StockRank120Direct'),('stock_rank60_direct','stock_rank120_direct'),('StockRank60Embedding','StockRank120Embedding'),('stock_rank60_embedding','stock_rank120_embedding'),('Rank60Mean','Rank120Mean'),('rank60mean','rank120mean'),('qa_v111','qa_v112'),('qa111','qa112'),('QA111','QA112'),('18149','18184')]:s=s.replace(old,new)
 s=re.sub(r'(?<!\d)(200|199|483|111)(?!\d)',lambda m:{'200':'201','199':'200','483':'484','111':'112'}[m.group()],s)
 s=s.replace('_v6_20261011','_v7_20261011').replace('__ACTUAL_PARENT_201__',PARENT)
 return s
NAMES=[changed(n) for n in template.NAMES]
EXTRAS=[changed(n) for n in template.EXTRAS[:19]]+[
 'stock_rank60_direct200_complete35_sources_admission_v6_20261011.json',
 *template.EXTRAS[20:22],
 'stock_rank120_new120_pipeline_admission_v1_20261011.json',
 'actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json',
 *template.EXTRAS[24:],
 'optimize_training_round201.py','finalize_training_round201.py']
def source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS]]))
def save(p,s):
 ast.parse(s)
 if p.exists():
  assert not (A/PROOF).exists(),'Cannot rewrite admitted sources'
 p.write_text(s,encoding='utf8');return p
def main():
 assert allowed();proof=read(A/template.PROOF)
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 assert read(A/'stock_rank120_new120_pipeline_admission_v1_20261011.json')['actual_CPU_cases']==31
 aliases=dict(zip(template.NAMES+template.EXTRAS[:12],NAMES+EXTRAS[:12]))
 aliases.update(dict(zip(template.EXTRAS[12:19],EXTRAS[12:19])))
 aliases.update({'prepare_StockRank60Direct200_complete35_pipeline_v6_20261011.py':FACTORY+'.py'})
 aliases.update({Path(k).stem:Path(v).stem for k,v in list(aliases.items()) if k.endswith('.py')})
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(aliases,key=len,reverse=True)));outputs=[];inputs=[]
 tokens={k:'__ALIAS_SENTINEL_'+chr(65+i%26)+chr(65+i//26)+'__' for i,k in enumerate(aliases)}
 for n in template.NAMES+template.EXTRAS[:9]:
  p=A/n;inputs.append(p);s=changed(pattern.sub(lambda m:tokens[m.group()],p.read_text(encoding='utf8')))
  for k,t in tokens.items():s=s.replace(t,aliases[k])
  s=s.replace('actual_stock_rank60_mature_objective_own6_full5_queue_v1_20261011','actual_stock_rank120_own6_full5_native42_direct33_queue_v2_20261011')
  # The new120 queue also includes scoring; the candidate family needs only its completed own bank.
  s=s.replace("closed('actual_stock_rank120_own6_full5_native42_direct33_queue_v2_20261011')","closed('actual_stock_rank120_embedding_small512_bank6_v1_20261011')")
  outputs.append(save(A/aliases[n],s))
 plan=read(A/template.EXTRAS[11]);plan.update(status='predeclared35_pure120_direct33_and_actual_complete183200_anchors_before_scores',expected_records=35,fully_qualified_anchors=[183,200],label_horizon_trading_days=120,loss_weighting='mature_rank120_Huber',families=[{'name':'StockRank120EmbeddingSmall512_after183_direct_allocation33','actual_service':'actual_stock_rank120_embedding_after183_direct_allocation33_v1_20261011','records':33,'base_round':183,'stage_kind':'stock_rank120_embedding_rank120mean_direct','main_receipt':'Rank120_after183_actual33_sources_main_receipt_v1_20261011.json'}])
 if (A/EXTRAS[11]).exists():assert read(A/EXTRAS[11])==plan
 else:create(A/EXTRAS[11],plan)
 # Explicit canonical adapters resolve publish() dynamic imports to the same pinned versioned modules.
 for index,canonical in [(2,'optimize_training_round201.py'),(3,'finalize_training_round201.py')]:outputs.append(save(A/canonical,'from '+Path(NAMES[index]).stem+' import *\n'))
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(201,200,(484,))
 normal=(A/EXTRAS[0]).read_text(encoding='utf8');assert 'for number in (183,200):' in normal and '(35,32,96)' in normal and "'stock_rank120_embedding_small512_BF16_bank6_v1_20261011'" in normal
 assert '(201, 112, 35)' in (A/NAMES[-1]).read_text(encoding='utf8')
 candidate=(A/EXTRAS[3]).read_text(encoding='utf8');assert 'parent_number in (183,200)' in candidate
 planned={'actual_stock_rank120_direct_embedding35_after200_normalization_queue_v7_20261011','StockRank120DirectEmbedding35_selected_native14_v7_20261011','StockRank120DirectEmbedding201_selected_candidate_preparation_v7_20261011','StockRank120DirectEmbedding201_selected_candidate_sealing_v7_20261011','actual_stock_rank120_embedding_six_state_native42_v1_20261011','StockRank120EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011','actual_stock_rank120_embedding_small512_bank6_v1_20261011'}
 gates=[]
 for p in outputs:
  for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
   if isinstance(node,ast.ImportFrom) and node.module and ('StockRank120Direct' in node.module or 'stock_rank120_direct' in node.module):assert (A/(node.module+'.py')).is_file(),(p.name,node.module)
   if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='closed' and node.args and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str):
    gate=node.args[0].value;assert gate in planned or (A/'service_owned_workflows_20261006'/gate/'native_launch.json').exists(),(p.name,gate);gates.append({'source':p.name,'gate':gate,'currently_owned_or_completed_service_file_exists':(A/'service_owned_workflows_20261006'/gate/'native_launch.json').exists(),'predeclared_future_gate':gate in planned})
 stage=importlib.import_module(Path(EXTRAS[14]).stem);norm=importlib.import_module(Path(EXTRAS[0]).stem);assert set(norm.RECIPES)==set(stage.BACKENDS)
 storage=importlib.import_module(Path(EXTRAS[2]).stem);assert len(storage.OUTPUTS)==6 and all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
 assert 'StockRank120DirectEmbedding201_selected_candidate_preparation_v7_20261011' in (A/EXTRAS[4]).read_text(encoding='utf8')
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/EXTRAS[11],*[A/n for n in EXTRAS[12:18]],*[A/n for n in EXTRAS[19:]]]}
 for n in (EXTRAS[9],EXTRAS[10],EXTRAS[18]):create(A/n,{'status':'compiled201_35_QA112_18184_W484_before_actual_selected_native_or_future','input_sha256':pins,'expected_records':35,'actual_future_X_read':False,'new_fits':0,'new_scores':0})
 create(A/PROOF,{'status':'compiled201_35_QA112_18184_W484_future_and_existing_waits_audited','input_sha256':pins,'expected_records':35,'expected_board':18184,'literal_wait_gates':gates,'new_fits':0,'new_scores':0,'test_labels_read':False})
 assert all(p.is_file() for p in source_paths())
 for name,driver in [('actual_stock_rank120_direct_embedding35_after200_normalization_queue_v7_20261011',EXTRAS[0]),('StockRank120DirectEmbedding35_selected_native14_v7_20261011',EXTRAS[1]),('StockRank120DirectEmbedding201_complete35_family_v7_20261011',EXTRAS[5])]:
  assert allowed();r=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),r)
 print({'actual201_sources_and_three_helpers_queued':True,'new_fits_or_scores_by_factory':0,'all_scientific_and_future_checks_pending':True},flush=True)
if __name__=='__main__':main()
