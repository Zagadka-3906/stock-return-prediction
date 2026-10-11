from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py'
 proofs=[A/n for n in ['actual183_inner_completion_recovery_routes_v15_20261011.json','cached149_39_27_exact_wrapper_recovery_routes_v16_20261011.json','rank10_rank20_higher_allocation49_predeclared_sources_admission_v1_20261011.json','stock_rank10_192_actual_materialized_source_controls_v1_20261011.json','stock_rank10_embedding192_full_execution_sources_admission_v1_20261011.json','rank10_192_canonical_terminal_dispatch_admission_v1_20261011.json','actual182_qualified_parent_prefix_bridge_verification_v1_20261011.json','actual183_completed_inner_inference_rehashed_recovery_v1_20261011.json']]
 paths=[Path(__file__),template,*proofs,A/'alias_actual_rank10_official46_completed_main_receipt_v1_20261011.py',A/'run_stock_rank10_objective_actual_stages_main_v3_20261011.py',A/'observer105_actual_idle104_supersession_admission_v1_20261011.json',A/'monitor_reboot_optimization_v105_20261011.py']
 for p in proofs:
  for name,d in read(p).get('input_sha256',{}).items():
   q=Path(name)
   if q.suffix in ('.py','.json'):assert sha(q)==d,q;paths.append(q)
 text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','HigherPotential95_routes15_16_sources')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start)
 text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
 manifest={'status':'actual_source_controls_and_queued95_higher_potential_cases_only','new_fits_or_scores_by_publication':0,'rank10_mean_horizon':10,'new_own_annual_fits_running_not_completed':True,'expected_new_rank10_cases':46,'expected_cached_rank10_rank20_higher_allocation_cases':49,'completed_prior_cached_cases':209,'actual183_inner_candidate_rehashed_and_sealed':True,'full183_registration_pending':True,'true_stock_count':4650,'sources192_48_QA103_17801_W475_independently_checked':True,'old_failures_preserved':True,'test_labels_read':False,'future_X_read_for_model_selection':False}
 text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 text=text.replace('新十日平均收益排名股票身份模型：7项独立均值排名与严格成熟未来投毒CPU检查通过；原生与独立解码器冻结，尚未训练或评分','十日成熟排序目标与大权重十日二十日融合95项候选源冻结：记录实际检查，训练评分仍在进行；保存15和16恢复来源')
 driver=A/'publish_higher_potential95_routes15_16_sources_main_v1_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
 r=start_service('actual_higher_potential95_routes15_16_sources_main_v1_20261011',driver.name,[],{str(driver):sha(driver)});create(A/'actual_higher_potential95_routes15_16_sources_main_activation_v1_20261011.json',r)
if __name__=='__main__':main()
