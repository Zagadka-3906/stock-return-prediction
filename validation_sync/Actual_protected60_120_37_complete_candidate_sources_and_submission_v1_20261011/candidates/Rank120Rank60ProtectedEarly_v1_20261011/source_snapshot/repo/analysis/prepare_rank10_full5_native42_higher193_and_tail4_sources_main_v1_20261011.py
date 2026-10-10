from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('StockRank10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011');closed('actual_stock_rank10_embedding_six_state_native42_v1_20261011');closed('actual_rank10_rank20_mixed_actual_eleven_parent_callbacks_CPU_v1_20261011');closed('actual_stock_rank20tail4_weighted_Huber_CPU_v1_20261011')
 template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py'
 proofs=[A/n for n in ['rank10_rank20_higher193_corrected_materialized_source_controls_v4_20261011.json','rank10_rank20_higher193_full_execution_sources_admission_v4_20261011.json','rank10_rank20_higher51_normalization_native14_sources_admission_v1_20261011.json','rank10_rank20_higher49_actual_native14_and_predictor_sources_admission_v1_20261011.json','rank10_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json','stock_rank20tail4_weighted_Huber_actual_CPU_controls_v1_20261011.json','stock_rank20tail4_embedding_own64_native_sources_preparation_v1_20261011.json','stock_rank20tail4_restart2_CPU_and_own6_queue_sources_admission_v3_20261011.json','stock_rank20tail4_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json','rank20tail4_actual_reused_fixture_gate_v1_20261011.json']]
 paths=[Path(__file__),template,*proofs]
 for proof in proofs:
  for p,d in read(proof).get('input_sha256',{}).items():
   assert sha(p)==d,p
   if Path(p).suffix in ('.py','.json'):paths.append(Path(p))
 for pointer in ['actual_StockRank10EmbeddingSmall512_full5_independent_location_v1_20261011.json','actual_stock_rank10_embedding_six_state_native42_location_v1_20261011.json']:
  p=A/pointer;v=Path(read(p)['output'])/'verification.json';paths.extend([p,v])
  assert read(v)['test_labels_read'] is False
 text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','Actual_Rank10_full5_native42_Higher193_Tail4_CPU6')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start)
 text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
 manifest={'status':'actual_rank10_own6_full5_native42_and_tail4_loss_CPU6_completed_sources_only','actual_rank10_own_fits':6,'actual_rank10_full_rows_days_stocks':[5635800,1212,4650],'actual_rank10_stage_native_cases':42,'actual_rank10_stage_cold_cases':42,'actual_rank10_prefit_refusals':7,'actual_higher_two_horizon_callback_checks':11,'actual193_corrected_materialized_source_checks':24,'actual_tail4_loss_scalar_CPU_checks':6,'tail4_own_fits_and_higher49_submission_qualification_pending':True,'new_scores_by_publication':0,'test_labels_read':False}
 text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 text=text.replace('新十日平均收益排名股票身份模型：7项独立均值排名与严格成熟未来投毒CPU检查通过；原生与独立解码器冻结，尚未训练或评分','十日排序模型：own6 full5 native42 cold42 prefit7完成；193完整51源检查通过；新增Top15标签权重4损失CPU6通过，未声明其训练评分完成')
 driver=A/'publish_Rank10_full5_native42_Higher193_Tail4_CPU6_sources_main_v1_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
 r=start_service('actual_Rank10_full5_native42_Higher193_Tail4_CPU6_sources_main_v1_20261011',driver.name,[],{str(driver):sha(driver)});create(A/'actual_Rank10_full5_native42_Higher193_Tail4_CPU6_sources_main_activation_v1_20261011.json',r)
if __name__=='__main__':main()
