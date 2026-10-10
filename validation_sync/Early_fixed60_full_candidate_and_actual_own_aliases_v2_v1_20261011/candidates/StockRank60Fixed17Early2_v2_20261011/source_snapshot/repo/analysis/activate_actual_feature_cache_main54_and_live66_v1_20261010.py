"""Observe real feature benchmark and publish measured evidence after conditional admission."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();source=A/'monitor_fast_optimization_v65_20261010.py';text=source.read_text(encoding='utf8').replace('progress_v65','progress_v66').replace('handoff_v113','handoff_v115').replace('rankings_v37','rankings_v38')
    needle='    while True:\n';assert text.count(needle)==1
    extra=['actual_feature120_verified_memoization_TRAIN344_v1_20261010','actual_full178_feature_cache_benchmark_admission_queue_v3_20261010','StockForward5Embedding178_complete48_family_v3_20261010','actual_feature120_benchmark_and_full178_runtime_main_v54_20261010']
    text=text.replace(needle,'    jobs += '+repr(extra)+'\n'+needle)
    text=text.replace("'StockForward5Embedding178_complete48_family_v2_20261010'):lines.append","'StockForward5Embedding178_complete48_family_v2_20261010','StockForward5Embedding178_complete48_family_v3_20261010'):lines.append")
    needle='        lines += [f"内存可用';assert text.count(needle)==1
    text=text.replace(needle,"        lines.append(f\"实际1599600行TRAIN特征缓存基准：{services['actual_feature120_verified_memoization_TRAIN344_v1_20261010']['status']}；仅在实际逐位一致且提速通过后，替换尚未派发的178轮推理入口。\")\n"+needle)
    observer=save('monitor_fast_optimization_v66_20261010.py',text)
    source=A/'publish_forward5_restart_full178_sources_main_v53_20261010.py';text=source.read_text(encoding='utf8');start=text.index('    paths=[');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    names=[Path(__file__).name,'exact_verified_feature120_memoization_runtime_v1_20261010.py','benchmark_exact_feature120_memoization_actual_TRAIN344_v1_20261010.py','run_StockForward5Embedding178_selected_candidate_feature_cache_v3_20261010.py','admit_full178_feature_cache_after_actual_benchmark_v3_20261010.py','monitor_fast_optimization_v66_20261010.py','actual_feature120_verified_memoization_TRAIN344_activation_v1_20261010.json','actual_full178_feature_cache_benchmark_admission_queue_activation_v3_20261010.json']
    replacement="    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed\n    closed('actual_full178_feature_cache_benchmark_admission_queue_v3_20261010')\n    pointer=A/'actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json'\n    actual=Path(read(pointer)['output']);benchmark=read(actual/'verification.json')\n    paths=[Path(__file__),pointer,*actual.glob('*.json'),*[A/n for n in "+repr(names)+"]]\n    for n in ('stock_forward5_embedding178_feature_cache_sources_admission_v3_20261010.json','stock_forward5_embedding178_feature_cache_not_adopted_v3_20261010.json','run_StockForward5Embedding178_complete_family_v3_20261010.py','actual_StockForward5Embedding178_complete48_family_feature_cache_activation_v3_20261010.json'):\n        if (A/n).exists():paths.append(A/n)\n"
    text=text[:start]+replacement+text[end:]
    text=text.replace('StockForward5Embedding_actual_restart_full178_sources','Feature120_actual_full_TRAIN344_cache_and_178_sources').replace('v53_20261010','v54_20261010').replace('passed_actual_forward5_return_small32_wide2_GPU_restart_smallCPU_nine_parent_callbacks_compiled_full17848_QA89_sources_annual_training_running_no_quality_claim','passed_actual1599600_TRAIN_feature120_native_Pandas_full_and_cold80_benchmark_conditional_idle178_runtime_admission_no_model_math_changed')
    text=text.replace("'forward5_quality_improvement_not_yet_established':True,","'actual_benchmark':benchmark,'new_quality_scores':0,")
    text=text.replace('保存五日收益股票嵌入实际GPU重启和独立CPU验证，以及48项选优冻结完整推理QA89 main来源；年度训练和正式评分进行中','保存实际1599600行TRAIN特征缓存逐位一致及速度基准，独立Pandas、cold80与输入变更核对；仅基准通过后接入未派发178轮推理')
    publisher=save('publish_actual_feature120_benchmark_and_full178_runtime_main_v54_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v65_20261010/native_launch.json'),'Replace exact childless observer65 with66 including real feature cache benchmark and conditional future dispatcher admission; scientific workers untouched')
    for name,p in [('actual_fast_optimization_progress_v66_20261010',observer),('actual_feature120_benchmark_and_full178_runtime_main_v54_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'live66_started':True,'actual_benchmark_completion_main54_queue_started':True},flush=True)
if __name__=='__main__':main()
