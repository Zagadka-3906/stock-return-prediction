from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def renamed(text):
 text=text.replace('near_refined','rank10_rank20_higher')
 text=re.sub(r'(?<![.\d])(25|27|24|72|190|191)(?!\d)',lambda m:{'25':'49','27':'51','24':'48','72':'144','190':'192','191':'193'}[m.group()],text)
 text=text.replace('StockRank20LongEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','StockRank10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011')
 text=text.replace('three_cached_mixed_stage_selector_and_CPU11_sources_admission_v2_20261011.json','rank10_rank20_higher49_actual_native14_and_predictor_sources_admission_v1_20261011.json')
 return text
def main():
 assert allowed();inputs=[];outputs=[]
 for name in ['normalize_completed_near_refined27_after190_v1_20261011.py','qualify_near_refined27_selected_native14_v1_20261011.py']:
  p=A/name;inputs.append(p);q=A/renamed(name);assert not q.exists();text=renamed(p.read_text(encoding='utf8'));compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n');outputs.append(q)
 plan=read(A/'near_refined_complete27_after190_plan_v1_20261011.json');plan.update(status='predeclared51_new_rank10_rank20_higher49_and175192_qualified_anchors_before_normalization',expected_records=51,fully_qualified_anchors=[175,192],actual_previous_complete_family='StockRank10Embedding192_complete48_family_v1_20261011',full193_factory_not_yet_created=True)
 plan.pop('full191_factory_not_yet_created',None)
 plan['families']=[{'name':'rank10_rank20_higher49','actual_service':'actual_rank10_rank20_after175_higher_allocation49_screen_v1_20261011','main_receipt':'Rank10Rank20_higher49_actual_official_sources_main_receipt_v1_20261011.json','output':'E:/赛题五_本机临时/StockRank10Rank20_after175_higher_allocation49_screen_v1_20261011','banks':['stock_rank20_embedding_small512_BF16_bank6_v1_20261010','stock_rank10_embedding_small512_BF16_bank6_v1_20261011'],'member_names':['Rank20_ID16_Cross120_seed20261009_e64','Rank10_ID16_Cross120_seed20261009_e64'],'native_stage_module':'rank10_rank20_mixed_after_qualified_parent_native_stage_v1_20261011','component_weight_field':'rank10_weight','component_weights':[.25,.5,.75],'label_horizons':[20,10],'training_windows':[252,252],'stage_kind':'rank10_rank20_mixed_raw_average','signal_name':'rank10_rank20_higher_two_horizon_raw_average'}]
 p=A/'rank10_rank20_higher_complete51_after192_plan_v1_20261011.json';create(p,plan)
 proof=A/'rank10_rank20_higher51_normalization_native14_sources_admission_v1_20261011.json'
 create(proof,{'status':'compiled_complete51_actual_case_capsule_rehash_normalization_and_selected_native14_before49_scores_complete','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,p,A/'rank10_rank20_higher49_actual_native14_and_predictor_sources_admission_v1_20261011.json',A/'rank10_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json']},'expected_records':51,'expected_full_controls':48,'expected_prefix_controls':144,'anchor_rounds':[175,192],'new_fits':0,'new_scores':0,'future_X_read':False,'test_labels_read':False})
 for name,p in [('actual_rank10_rank20_higher51_after192_normalization_v1_20261011',outputs[0]),('actual_rank10_rank20_higher51_selected_native14_v1_20261011',outputs[1])]:
  assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 print({'actual_higher49_plus175192_complete51_prerequisites_queued':True},flush=True)
if __name__=='__main__':main()
