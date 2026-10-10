from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('StockRank10Embedding_actual_mature_fixture_CPU_v1_20261011');closed('actual_stock_rank10_embedding_eleven_parent_callbacks_CPU_v1_20261011');closed('actual183_completed_inner_inference_rehashed_recovery_v1_20261011')
 pointer=A/'actual_stock_rank10_embedding_mature_fixture_location_v1_20261011.json';fixture=Path(read(pointer)['output'])/'verification.json'
 assert read(fixture)['rows']==49153 and read(fixture)['actual_future_label_poisoning_same_keys_and_targets']
 paths=list(dict.fromkeys([Path(__file__),pointer,fixture,A/'stock_rank10_embedding_actual_restart_and_own6_sources_admission_v1_20261011.json',A/'stock_rank10_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json',A/'rank10_fast46_and_actual183_inner_recovery_dispatch_v1_20261011.json',A/'stock_rank10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json',A/'actual183_completed_inner_inference_rehashed_recovery_v1_20261011.json',*[A/n for n in ['verify_stock_rank10_embedding_actual_mature_fixture_v1_20261011.py','verify_stock_rank10_embedding_small512_restart_v1_20261011.py','verify_stock_rank10_embedding_small512_small_CPU_v1_20261011.py','train_stock_rank10_embedding_small512_BF16_bank6_own64_v1_20261011.py','verify_stock_rank10_embedding_small512_full5_independent_v1_20261011.py','run_stock_rank10_embedding_own_training_and_full5_queue_v2_20261011.py','run_stock_rank10_native42_and_fast46_queue_v1_20261011.py']]]))
 for proof in ['stock_rank10_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json','stock_rank10_embedding_actual_restart_and_own6_sources_admission_v1_20261011.json']:
  for p,d in read(A/proof)['input_sha256'].items():assert sha(p)==d,p;paths.append(Path(p))
 source=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';text=source.read_text(encoding='utf8')
 text=text.replace('Rank10_actual_maturity7','Rank10_actual_fixture_callbacks11_fast46').replace('新十日平均收益排名股票身份模型：7项独立均值排名与严格成熟未来投毒CPU检查通过；原生与独立解码器冻结，尚未训练或评分','十日排序模型：49153真实成熟样本与11父方案回调CPU验证通过，独立六年度训练及46融合评分源冻结；尚未完成训练评分')
 replacement='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n    import publish_classifier'
 text=re.sub(r"    paths=\[.*?\]\]\n    import publish_classifier",lambda m:replacement,text,count=1,flags=re.S)
 text=text.replace("'actual_CPU_checks': 7","'actual_mature_fixture_rows': 49153, 'actual_callback_CPU_checks': 11")
 text=text.replace('actual7_independent_ten_day_label_maturity_CPU_checks_passed_new_rank10_native_decoder_compiled','actual49153_mature_fixture_and11_callbacks_passed_new_rank10_own6_training_sources46_screen_frozen')
 driver=A/'publish_Rank10_actual_fixture_callbacks11_fast46_sources_main_v2_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
 assert "49153" in text and str(fixture).replace('\\','\\\\') in text
 r=start_service('actual_Rank10_actual_fixture_callbacks11_fast46_sources_main_v1_20261011',driver.name,[],{str(driver):sha(driver)});create(A/'actual_Rank10_actual_fixture_callbacks11_fast46_sources_main_activation_v1_20261011.json',r)
if __name__=='__main__':main()
