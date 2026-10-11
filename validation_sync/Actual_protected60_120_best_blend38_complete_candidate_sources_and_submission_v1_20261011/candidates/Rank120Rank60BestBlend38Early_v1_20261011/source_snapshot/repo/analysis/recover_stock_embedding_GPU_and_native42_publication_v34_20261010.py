"""Rebuild exact existing publication paths; preserve the failed pre-mutation prototype."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    failed=A/'service_owned_workflows_20261006/actual_stock_embedding_GPU_restart_and_checkpoint_yield_main_v33_20261010/service_execution.json'
    assert read(failed)['status']=='failed' and 'FileNotFoundError' in read(failed)['failure']
    original=A/'publish_stock_embedding_actual_GPU_restart_and_checkpoint_yield_v33_20261010.py';text=original.read_text(encoding='utf8')
    begin=text.index('    paths=[Path(p) for p in ');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    dynamic="""    restart=Path(read(A/'actual_stock_embedding_small512_restart_location_v1_20261010.json')['output'])
    assert read(restart/'verification.json')['status']=='passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart'
    small=Path('E:/赛题五_本机临时/StockEmbeddingSmall512_independent_small_CPU_v1_20261009')
    paths=[Path(__file__),*A.glob('*stock_embedding*.py'),*A.glob('*stock_embedding*admission*.json'),*A.glob('*stock_embedding*activation*.json'),A/'actual_optimization_fast_runtime_handoff_v74_20261010.json',A/'observers44_and45_retired_after_actual46_verified_v1_20261010.json',A/'stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1_20261010.json',A/'actual_stock_embedding_small512_restart_location_v1_20261010.json',*restart.glob('*.json'),*restart.glob('*/*.json'),*small.glob('*.json')]
    assert all(p.is_file() for p in paths)
"""
    text=text[:begin]+dynamic+text[end:]
    for token in ('preparation_v33','preparation_main_v33','preparation_main_receipt_v33'):text=text.replace(token,token.replace('v33','v34'))
    pub=save('publish_stock_embedding_actual_GPU_restart_and_checkpoint_yield_v34_20261010.py',text)
    row=start_service('actual_stock_embedding_GPU_restart_and_checkpoint_yield_main_v34_20261010',pub.name,[],{str(pub):sha(pub)})
    create(A/'actual_stock_embedding_GPU_restart_and_checkpoint_yield_main_activation_v34_20261010.json',row)
    begin=text.index("    restart=Path(read(");end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
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
    text=text.replace('stock_embedding_actual_GPU_restart_and_checkpoint_yield_preparation','stock_embedding_actual_six_state_native42_completion')
    for token in ('completion_v34','completion_main_v34','completion_main_receipt_v34'):text=text.replace(token,token.replace('v34','v50'))
    text=text.replace('passed_actual_two_stock_embedding_fresh_process_GPU_restart_controls_saved_tensors_exact_four_parent_CPU_hooks_checkpoint_yield_training_active_quality_pending','passed_actual_stock_embedding_six_full_annual_fits_5635800_independent_predictions42_native42_cold7_prefit_refusals_quality_and_full_candidate_pending')
    text=text.replace('保存股票嵌入网络两项实际GPU断点续训、独立解码与四种完整父模型回调检查，利用空闲GPU按8epoch检查点让位加速训练','保存新股票嵌入模型六年度训练和完整5635800行独立预测、42项原生42项冷启动及7项拟合前拒绝控制，官方提分和提交资格待完成')
    completion=save('publish_stock_embedding_six_state_native42_completion_v50_20261010.py',text)
    row=start_service('actual_stock_embedding_six_state_native42_completion_main_v50_20261010',completion.name,[],{str(completion):sha(completion)})
    create(A/'actual_stock_embedding_six_state_native42_completion_main_activation_v50_20261010.json',row)
    create(A/'stock_embedding_safe_publication_exact_existing_paths_recovery_v34_20261010.json',{'status':'failed33_pre_git_mutation_record_preserved_exact_existing_source_inventory34_and_native42_completion50_launched','input_sha256':{str(p):sha(p) for p in [Path(__file__),original,failed,pub,completion]},'new_quality_scores':0,'original33_failed_before_git_mutation':True})
    print('Actual34 exact-existing-path publisher and actual50 native42 completion publisher launched',flush=True)
if __name__=='__main__':main()
