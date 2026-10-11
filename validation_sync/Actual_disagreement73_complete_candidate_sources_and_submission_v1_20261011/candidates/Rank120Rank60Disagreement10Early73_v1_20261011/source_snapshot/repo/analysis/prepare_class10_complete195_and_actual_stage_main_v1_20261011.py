from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def save(p,s):
 assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p
def main():
 assert allowed();old=A/'prepare_StockRank20Tail4Embedding194_complete48_pipeline_v1_20261011.py'
 s=old.read_text(encoding='utf8').replace('StockRank20Tail4','StockRank20Class10').replace('stock_rank20tail4','stock_rank20class10').replace('rank20tail4','rank20class10').replace('STOCK_RANK20TAIL4','STOCK_RANK20CLASS10')
 s=s.replace('17900','17948').replace('qa105','qa106').replace('QA105','QA106').replace('qa_v105','qa_v106')
 s=re.sub(r'(?<!\d)(194|193|477|105)(?!\d)',lambda m:{'194':'195','193':'194','477':'478','105':'106'}[m.group()],s)
 s=s.replace("'rank10_rank20_higher194_full_execution_sources_admission_v4_20261011.json'","'stock_rank20tail4_embedding194_full_execution_sources_admission_v1_20261011.json'")
 s=s.replace("'Rank10Rank20Higher194_complete51_family_v4_20261011'","'StockRank20Tail4Embedding194_complete48_family_v1_20261011'")
 s=s.replace("'actual_stock_rank20class10_own_training_and_full5_queue_v3_20261011'","'actual_stock_rank20class10_BCE_own6_full5_queue_v1_20261011'")
 s=s.replace("loss_weighting='label_rank_upper15_linear_tail4'","loss_weighting='balanced_mature_rank20_top10_binary'").replace("=='label_rank_upper15_linear_tail4'","=='balanced_mature_rank20_top10_binary'")
 # Generated full-registration jobs use the already verified reboot identity and external frozen capsules.
 needle="  # Screen folders are actual October11 outputs, unlike the legacy template suffix."
 inject="""  text=text.replace('from owned_idle_publication_wait_runtime_v1_20261010 import hold','from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold').replace('from publish_explicit_parent_training_round_v2_20261005 import publish','from publish_explicit_parent_training_round_external_frozen_v3_20261011 import publish')
"""
 assert needle in s;s=s.replace(needle,inject+needle)
 factory=save(A/'prepare_StockRank20Class10Embedding195_complete48_pipeline_v1_20261011.py',s)
 oldstage=A/'run_stock_rank20tail4_objective_actual_stages_main_v2_20261011.py';s=oldstage.read_text(encoding='utf8').replace('stock_rank20tail4','stock_rank20class10').replace('StockRank20Tail4','StockRank20Class10').replace('stockrank10','stockrank20class10').replace('restart_v2','restart_v1').replace('actual_completed_rank10_stage_only','actual_completed_mature20_top10_balanced_BCE_stage_only').replace('mean20_maturity_reused_and_new_weighted_loss_CPU6_passed','mean20_maturity_reused_and_balanced_BCE_CPU6_gradient_passed')
 s=s.replace('publish_StockRank20Class10_objective_{stage}_main_v3_','publish_frozen_StockRank20Class10_objective_{stage}_main_v1_')
 stage=save(A/'run_stock_rank20class10_objective_actual_stages_main_v1_20261011.py',s)
 # All future children retain actual parent34 closure; scientific input bytes are unchanged.
 wrapper=save(A/'run_StockRank20Class10Embedding195_actual_parent34_factory_v1_20261011.py',"from pathlib import Path\nimport sys,importlib,runpy\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom run_dependency_queue_v3_20261006 import read,sha\nfrom prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed\nfrom route_new_objectives_exact_source_recovery34_v1_20261011 import installed\nif __name__=='__main__':\n assert allowed();closed,start,data=installed()\n import prepare_StockRank20Class10Embedding195_complete48_pipeline_v1_20261011 as m\n prior=m.source_paths\n m.source_paths=lambda:list(dict.fromkeys([*prior(),A/'new_objectives_exact_source_recovery34_routes_v1_20261011.json',Path(__file__)]))\n import start_fast_completed_owned_service_v1_20261011 as fast\n original=fast.start_service\n def dispatch(name,driver,args,pins):\n  path=A/driver\n  if 'StockRank20Class10' in driver or 'stock_rank20class10' in driver:\n   q=A/(path.stem+'_actual_parent34_dispatch_wrapper.py')\n   if not q.exists():\n    text=\"from pathlib import Path\\nimport sys,runpy\\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\\nfrom route_new_objectives_exact_source_recovery34_v1_20261011 import installed\\nif __name__=='__main__':\\n closed,start,data=installed()\\n runpy.run_path(str(A/\"+repr(driver)+\"),run_name='__main__')\\n\"\n    compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\\n')\n   return original(name,q.name,args,{**pins,str(q):sha(q)})\n  return original(name,driver,args,pins)\n m.start_service=dispatch\n import handoff_ready_goss_full_execution_20261006 as launch\n launch.start_service=dispatch\n m.main()\n")
 proof=A/'stock_rank20class10_complete195_actual_parent34_pipeline_sources_v1_20261011.json';paths=[Path(__file__),old,oldstage,factory,stage,wrapper,A/'new_objectives_exact_source_recovery34_routes_v1_20261011.json'];create(proof,{'status':'compiled_complete195_QA106_17948_W478_and_staged_actual_BCE_publication_before_scores','input_sha256':{str(p):sha(p) for p in paths},'new_fits':0,'new_scores':0,'future_X_read':False})
 for name,p in [('actual_stock_rank20class10_objective_stages_main_v1_20261011',stage),('actual_stock_rank20class10_complete195_factory_v1_20261011',wrapper)]:
  assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
 print({'class10_complete195_factory_and_stage_publication_queued':True},flush=True)
if __name__=='__main__':main()
