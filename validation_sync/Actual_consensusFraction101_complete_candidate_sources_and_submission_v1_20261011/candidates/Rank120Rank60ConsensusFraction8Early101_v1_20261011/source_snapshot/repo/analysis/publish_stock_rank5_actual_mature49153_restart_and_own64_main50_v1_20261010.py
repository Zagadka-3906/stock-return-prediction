"""Publish real rank5 mature alignment and GPU restart before annual quality claims."""
from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed
    closed('actual_stock_rank5_embedding_small512_restart_v1_20261010');closed('StockRank5EmbeddingSmall512_independent_small_CPU_v1_20261009')
    pointer=A/'actual_stock_rank5_embedding_mature_fixture_location_v1_20261010.json';fixture=Path(read(pointer)['output']);assert read(fixture/'verification.json')['rows']==49153
    restart=Path(read(A/'actual_stock_rank5_embedding_small512_restart_location_v1_20261010.json')['output']);assert read(restart/'verification.json')['status']=='passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart'
    small=Path('E:/赛题五_本机临时/StockRank5EmbeddingSmall512_independent_small_CPU_v1_20261009')
    template=A/'publish_Top10_full176_sources_actual_main_v49_20261010.py';text=template.read_text(encoding='utf8');tree=ast.parse(text);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main');node=next(n for n in fn.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='paths'for t in n.targets))
    names=['stock_identity_rank5_own64_prospective_direction_plan_v1_20261010.json','prepare_stock_rank5_embedding_own64_native_and_fixture_v1_20261010.py','verify_stock_rank5_embedding_actual_mature_fixture_v1_20261010.py','stock_rank5_embedding_small512_BF16_native_v1_20261010.py','stock_rank5_embedding_saved_tensor_decoder_v1_20261010.py','stock_rank5_embedding_own64_native_sources_preparation_v1_20261010.json','prepare_stock_rank5_embedding_actual_restart_and_own6_v1_20261010.py','verify_stock_rank5_embedding_small512_restart_v1_20261010.py','verify_stock_rank5_embedding_small512_small_CPU_v1_20261010.py','train_stock_rank5_embedding_small512_BF16_bank6_own64_v1_20261010.py','stock_rank5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json','run_stock_rank5_embedding_own_training_queue_v1_20261010.py','prepare_stock_rank5_embedding_full5_native42_and_early17_v1_20261010.py','verify_stock_rank5_embedding_small512_full5_independent_v1_20261010.py','stock_rank5_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','verify_stock_rank5_embedding_six_state_native42_v1_20261010.py','run_stock_rank5_embedding_after171_fast17_screen_v1_20261010.py','stock_rank5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json','run_stock_rank5_embedding_full5_native42_and_early17_queue_v1_20261010.py','prepare_rank5_completion_publishers_and_live62_v1_20261010.py','publish_stock_rank5_embedding_six_state_native42_completion_v64_20261010.py','publish_stock_rank5_embedding_after171_completion_v63_20261010.py','monitor_fast_optimization_v62_20261010.py','actual_fast_optimization_progress_v62_activation_20261010.json']
    paths=[Path(__file__),template,pointer,*[A/n for n in names],*fixture.glob('*.json'),*restart.rglob('*.json'),*small.glob('*.json')]
    for n in ('StockRank5Embedding_actual_mature_fixture_CPU_v1_20261010','actual_stock_rank5_embedding_small512_restart_v1_20261010','StockRank5EmbeddingSmall512_independent_small_CPU_v1_20261009'):
        paths += [A/'service_owned_workflows_20261006'/n/f for f in ('native_launch.json','service_execution.json','job_definition.json')]
    assert all(p.exists()for p in paths)
    lines=text.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths='+repr([str(p)for p in paths])+'\n'];text=''.join(lines)
    for old,new in [('StockTop10Embedding_verified_BCE_loss_and_runtime_v49_20261010','StockRank5Embedding_actual_mature49153_restart_own64_v50_20261010'),('StockTop10Embedding_verified_BCE_loss_and_runtime_main_v49_20261010','StockRank5Embedding_actual_mature49153_restart_own64_main_v50_20261010'),('StockTop10Embedding_verified_BCE_loss_and_runtime_main_receipt_v49_20261010','StockRank5Embedding_actual_mature49153_restart_own64_main_receipt_v50_20261010')]:text=text.replace(old,new)
    text=text.replace('compiled_full176_31_normalizer_selected14_candidate_freeze_registry_QA87_main_sources_actual_early171_29_scoring_running','passed_actual_rank5_mature49153_feature121_alignment_exact_once_centering_GPU_small32_wide2_restart_independent_smallCPU_own64_annual_fits_running_no_quality_scores_claimed')
    text=text.replace('保存第176轮31项比较、独立原生检查、冻结和两次完整推理至QA87及main交付来源；提前171轮29项评分进行中，不遗漏可能优于175轮的方案','保存股票身份嵌入与五日收益排名的新64epoch训练来源；真实49153成熟标签与121输入对齐、仅居中一次、GPU重启逐位一致性和独立CPU解码已通过，年度训练进行中，未声明官方提分')
    driver=A/'publish_stock_rank5_actual_mature49153_restart_own64_actual_main_v50_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_stock_rank5_actual_mature49153_restart_own64_main_v50_20261010',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_stock_rank5_actual_mature49153_restart_own64_main_activation_v50_20261010.json',row);print({'actual_rank5_mature_and_GPU_batch_main50_worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
