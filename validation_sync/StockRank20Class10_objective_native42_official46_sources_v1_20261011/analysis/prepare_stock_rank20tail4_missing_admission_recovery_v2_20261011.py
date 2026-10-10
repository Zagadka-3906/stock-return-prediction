from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();source=A/'stock_rank20tail4_own64_native_sources_preparation_v1_20261011.json';v=read(source)
 for p,d in v['input_sha256'].items():assert sha(p)==d,p
 assert v['configuration']['loss_weighting']=='label_rank_upper15_linear_tail4'
 create(A/'stock_rank20tail4_embedding_own64_native_sources_preparation_v1_20261011.json',v)
 failure=A/'service_owned_workflows_20261006/actual_stock_rank20tail4_embedding_small512_restart_v1_20261011/service_execution.json'
 assert read(failure)['status']=='failed' and 'own64_native_sources_preparation' in read(failure)['failure']
 out=Path('E:/赛题五_本机临时/GPU实测_20261009/stock_rank20tail4_embedding_small512_restart_v1_20261011')
 assert not list(out.rglob('*.joblib')) and not (out/'frozen_before_actual_controls.json').exists()
 outputs=[]
 def save(old,new,transform):
  p=A/old;q=A/new;assert not q.exists();t=transform(p.read_text(encoding='utf8'));compile(t,str(q),'exec');q.write_text(t,encoding='utf8',newline='\n');outputs.append(q);return q
 restart=save('verify_stock_rank20tail4_embedding_small512_restart_v1_20261011.py','verify_stock_rank20tail4_embedding_small512_restart_v2_20261011.py',lambda t:t)
 trainer=save('train_stock_rank20tail4_embedding_small512_BF16_bank6_own64_v1_20261011.py','train_stock_rank20tail4_embedding_small512_BF16_bank6_own64_v2_20261011.py',lambda t:t.replace('actual_stock_rank20tail4_embedding_small512_restart_v1_20261011','actual_stock_rank20tail4_embedding_small512_restart_v2_20261011'))
 queue=save('run_stock_rank20tail4_own_training_and_full5_queue_v1_20261011.py','run_stock_rank20tail4_own_training_and_full5_queue_v2_20261011.py',lambda t:t.replace('actual_stock_rank20tail4_embedding_small512_restart_v1_20261011','actual_stock_rank20tail4_embedding_small512_restart_v2_20261011').replace('verify_stock_rank20tail4_embedding_small512_restart_v1_20261011.py',restart.name).replace('train_stock_rank20tail4_embedding_small512_BF16_bank6_own64_v1_20261011.py',trainer.name))
 publisher=save('run_stock_rank20tail4_objective_actual_stages_main_v1_20261011.py','run_stock_rank20tail4_objective_actual_stages_main_v2_20261011.py',lambda t:t.replace('actual_stock_rank20tail4_embedding_small512_restart_v1_20261011','actual_stock_rank20tail4_embedding_small512_restart_v2_20261011'))
 proof=A/'rank20tail4_actual_pre_fit_missing_admission_recovery_v2_20261011.json'
 create(proof,{'status':'compiled_missing_source_admission_alias_and_fresh_restart_before_any_GPU_fit','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,A/'stock_rank20tail4_embedding_own64_native_sources_preparation_v1_20261011.json',failure,*outputs]},'prior_restart_failed_before_any_model_fit':True,'original_failure_preserved':True,'new_fits':0,'new_scores':0})
 for name,p in [('actual_stock_rank20tail4_own_training_and_full5_queue_v2_20261011',queue),('actual_stock_rank20tail4_objective_stages_main_v2_20261011',publisher)]:
  assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 print({'tail4_missing_admission_recovered_before_any_fit':True},flush=True)
if __name__=='__main__':main()
