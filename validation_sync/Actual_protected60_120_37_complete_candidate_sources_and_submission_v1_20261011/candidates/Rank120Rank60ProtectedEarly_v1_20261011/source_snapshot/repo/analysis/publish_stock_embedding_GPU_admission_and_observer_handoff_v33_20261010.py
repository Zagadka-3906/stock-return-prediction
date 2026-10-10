"""Freeze and publish the passed actual GPU controls and faster checkpoint-yield dispatcher."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();state=read(A/'optimization_live_progress_v46_20261010.json')
    assert 'actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010' in state['services']
    retired=[]
    for version in (44,45):
        name=f'actual_fast_optimization_progress_v{version}_20261010';row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json')
        retire(row,'Actual observer46 verified; retire duplicate childless observers and keep all scoring, training, inference and guardian processes.')
        retired.append(row)
    create(A/'observers44_and45_retired_after_actual46_verified_v1_20261010.json',{'status':'administratively_retired_duplicate_observers_only','retired':retired,'actual_successor':'actual_fast_optimization_progress_v46_20261010','scientific_tasks_terminated':0})
    restart=Path(read(A/'actual_stock_embedding_small512_restart_location_v1_20261010.json')['output'])
    assert read(restart/'verification.json')['status']=='passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart'
    small=Path('E:/赛题五_本机临时/StockEmbeddingSmall512_independent_small_CPU_v1_20261009')
    assert read(small/'verification.json')['status'].startswith('passed')
    handoff={'status':'active_actual_stock_embedding_checkpoint_yield_training_and_native42_plus_existing193_81_49_and_complete171_172','deadline_local':state['deadline_local'],'best_fully_qualified':state['best_fully_qualified'],'actual_live_progress':str(A/'optimization_live_progress_v46_20261010.json'),'stock_new_gpu_controls':str(restart/'verification.json'),'stock_checkpoint_yield_actual_service':'actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010','stock_actual_six_fit_service':'actual_stock_embedding_small512_bank6_v1_20261010','stock_native42_actual_service':'actual_stock_embedding_six_state_native42_v2_20261010','stock17_actual_screen_service':'actual_stock_embedding_after172_high_impact17_screen_v1_20261010','stock17_expected_main_service':'actual_stock_embedding17_completion_main_v49_20261010','stock_own_gpu_restart_and_CPU_controls':'passed_actual_two_fresh_process_restart_cases_independent_GPU_decoding_and_real_mature_stock_unknown_mapping','stock_own_training_and_quality_complete':False,'stock_full_candidate173_flow':'not_created_pending_actual17_results_and_selected_stage_qualification','all_existing_scoring_and_candidate_services_preserved':True,'latest_CPU_admission_main_receipt':read(A/'stock_embedding_actual_CPU_and_predeclared17_preparation_main_receipt_v32_20261010.json')}
    create(A/'actual_optimization_fast_runtime_handoff_v74_20261010.json',handoff)
    paths=[Path(__file__),A/'actual_optimization_fast_runtime_handoff_v74_20261010.json',A/'observers44_and45_retired_after_actual46_verified_v1_20261010.json',*A.glob('*stock_embedding*.py'),*A.glob('*stock_embedding*admission*.json'),*A.glob('*stock_embedding*activation*.json'),A/'actual_fast_optimization_progress_v46_activation_20261010.json',A/'monitor_fast_optimization_v46_20261010.py',A/'stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1_20261010.json',A/'actual_stock_embedding_small512_restart_location_v1_20261010.json',*restart.glob('*.json'),*restart.glob('*/*.json'),*small.glob('*.json')]
    original=A/'publish_stock_embedding_actual_CPU_preparation_v32_20261010.py';text=original.read_text(encoding='utf8')
    begin=text.index('    paths=[Path(p) for p in ');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    text=text[:begin]+'    paths=[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']\n'+text[end:]
    text=text.replace('stock_embedding_actual_CPU_and_predeclared17_preparation','stock_embedding_actual_GPU_restart_and_checkpoint_yield_preparation').replace('v32_20261010','v33_20261010')
    text=text.replace('passed_actual_mature49153_stock_identity_mapping_and_independent_CPU10017_four_prefixes_new_GPU_restart_and_17_quality_cases_queued','passed_actual_two_stock_embedding_fresh_process_GPU_restart_controls_saved_tensors_exact_four_parent_CPU_hooks_checkpoint_yield_training_active_quality_pending')
    text=text.replace('保存新股票身份嵌入小网络的49153行成熟训练映射与10017行CPU独立推理、未知股票与四个前缀检查，以及预声明17项提分快速验证队列','保存股票嵌入网络两项实际GPU断点续训、独立解码与四种完整父模型回调检查，利用空闲GPU按8epoch检查点让位加速训练')
    publisher=save('publish_stock_embedding_actual_GPU_restart_and_checkpoint_yield_v33_20261010.py',text)
    assert allowed();row=start_service('actual_stock_embedding_GPU_restart_and_checkpoint_yield_main_v33_20261010',publisher.name,[],{str(publisher):sha(publisher)})
    create(A/'actual_stock_embedding_GPU_restart_and_checkpoint_yield_main_activation_v33_20261010.json',row)
    #Publish six-state controls independently as soon as the batch truly finishes.
    begin=text.index('    paths=[Path(p) for p in ');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    dynamic="""    closed('actual_stock_embedding_six_state_native42_v2_20261010')
    pointer=A/'actual_stock_embedding_six_state_native42_location_v1_20261010.json'
    folder=Path(read(pointer)['output']);proof=read(folder/'verification.json')
    assert proof['actual_native_cases']==42 and proof['actual_cold_cases']==42 and len(proof['prefit_rejections'])==7
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    paths=[Path(__file__),pointer,*folder.glob('*.json'),*[Path(p) for p in proof['input_sha256'] if Path(p).suffix=='.py'],A/'stock_embedding_native_stage_and_four_parent_routes_admission_v1_20261010.json']
    bank=Path(read(A/'actual_stock_embedding_small512_bank6_location_v1_20261010.json')['output'])
    paths += [bank/'verification.json',*bank.glob('*/info.json')]
    full=Path(read(A/'actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json')['output'])
    paths += [*full.glob('*.json')]
"""
    text=text[:begin]+dynamic+text[end:]
    text=text.replace('stock_embedding_actual_GPU_restart_and_checkpoint_yield_preparation','stock_embedding_actual_six_state_native42_completion').replace('v33_20261010','v50_20261010')
    text=text.replace('passed_actual_two_stock_embedding_fresh_process_GPU_restart_controls_saved_tensors_exact_four_parent_CPU_hooks_checkpoint_yield_training_active_quality_pending','passed_actual_stock_embedding_six_full_annual_fits_5635800_independent_predictions42_native42_cold7_prefit_refusals_quality_and_full_candidate_pending')
    text=text.replace('保存股票嵌入网络两项实际GPU断点续训、独立解码与四种完整父模型回调检查，利用空闲GPU按8epoch检查点让位加速训练','保存新股票嵌入模型六年度训练和完整5635800行独立预测、42项原生42项冷启动及7项拟合前拒绝控制，官方提分和提交资格待完成')
    completion=save('publish_stock_embedding_six_state_native42_completion_v50_20261010.py',text)
    assert allowed();row=start_service('actual_stock_embedding_six_state_native42_completion_main_v50_20261010',completion.name,[],{str(completion):sha(completion)})
    create(A/'actual_stock_embedding_six_state_native42_completion_main_activation_v50_20261010.json',row)
    print('Duplicate observers retired; actual GPU proof main publication and native42 batch completion publication launched',flush=True)
if __name__=='__main__':main()
