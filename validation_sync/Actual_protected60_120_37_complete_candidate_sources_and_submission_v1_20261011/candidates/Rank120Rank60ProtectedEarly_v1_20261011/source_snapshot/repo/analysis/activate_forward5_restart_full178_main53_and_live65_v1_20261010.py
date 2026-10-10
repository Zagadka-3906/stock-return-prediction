"""Publish actual GPU controls and prospective full178 sources; monitor all new work."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();closed('StockForward5EmbeddingSmall512_independent_small_CPU_v1_20261009')
    source=A/'monitor_fast_optimization_v64_20261010.py';text=source.read_text(encoding='utf8').replace('progress_v64','progress_v65').replace('handoff_v111','handoff_v113').replace('rankings_v36','rankings_v37')
    extra=['actual_stock_forward5_embedding_full5_native42_and_early17_queue_v1_20261010','StockForward5EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_forward5_embedding_six_state_native42_v1_20261010','actual_stock_forward5_embedding_after171_fast17_screen_v1_20261010','actual_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010','actual_stock_forward5_embedding_six_state_native42_completion_main_v67_20261010','actual_stock_forward5_embedding_after171_completion_main_v66_20261010','actual_stock_forward5_embedding_after171_large29_completion_main_v68_20261010','actual_stock_forward5_embedding48_after177_normalization_queue_v2_20261010','StockForward5Embedding48_selected_native14_v2_20261010','StockForward5Embedding178_complete48_family_v2_20261010','StockForward5Embedding178_selected_candidate_preparation_v1_20261010','StockForward5Embedding178_selected_candidate_sealing_v1_20261010','StockForward5Embedding178_round178_full_registration_v1_20261010','actual_forward5_restart_full178_sources_main_v53_20261010']
    needle='    while True:\n';assert text.count(needle)==1;text=text.replace(needle,'    jobs += '+repr(extra)+"\n    families += ['StockForward5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010','StockForward5EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010']\n"+needle)
    needle="('StockRank5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010',17)"
    text=text.replace(needle,"('StockForward5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010',17),('StockForward5EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010',29),"+needle)
    text=text.replace("'StockRank5Embedding177_complete48_family_v2_20261010'):lines.append","'StockRank5Embedding177_complete48_family_v2_20261010','StockForward5Embedding178_complete48_family_v2_20261010'):lines.append")
    observer=save('monitor_fast_optimization_v65_20261010.py',text)
    source=A/'publish_forward5_actual_CPU_sources_main_v52_20261010.py';text=source.read_text(encoding='utf8');start=text.index('    paths=[');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    from prepare_StockForward5Embedding178_complete48_pipeline_v1_20261010 import NAMES,EXTRAS
    names=list(dict.fromkeys([*NAMES,*EXTRAS,'stock_forward5_embedding178_full_registry_sources_preparation_v2_20261010.json','stock_forward5_embedding178_full_execution_sources_admission_v2_20261010.json','run_StockForward5Embedding178_complete_family_v2_20261010.py','run_StockForward5Embedding178_full_registration_v2_20261010.py','verify_StockForward5Embedding178_full48_preflight_v2_20261010.py','monitor_fast_optimization_v65_20261010.py',Path(__file__).name,'publish_stock_forward5_embedding_six_state_native42_completion_v67_20261010.py','publish_stock_forward5_embedding_after171_completion_v66_20261010.py','publish_stock_forward5_embedding_after171_large29_completion_v68_20261010.py','stock_forward5_embedding_own64_native_sources_preparation_v1_20261010.json','stock_forward5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json']))
    paths=[A/n for n in names]
    for proof in ('stock_forward5_embedding_own64_native_sources_preparation_v1_20261010.json','stock_forward5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json','stock_forward5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'):
        paths += [A/proof,*[Path(p) for p in read(A/proof)['input_sha256'] if Path(p).suffix=='.py']]
    restart=Path(read(A/'actual_stock_forward5_embedding_small512_restart_location_v1_20261010.json')['output'])
    paths += list(restart.rglob('*.json'))+list(Path('E:/赛题五_本机临时/StockForward5EmbeddingSmall512_independent_small_CPU_v1_20261009').glob('*.json'))
    for job in ('actual_stock_forward5_embedding_small512_restart_v1_20261010','StockForward5EmbeddingSmall512_independent_small_CPU_v1_20261009'):
        paths += [A/'service_owned_workflows_20261006'/job/n for n in ('native_launch.json','service_execution.json','job_definition.json')]
    assert all(p.is_file() for p in paths)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
    text=text.replace('StockForward5Embedding_actual_mature_CPU_sources','StockForward5Embedding_actual_restart_full178_sources').replace('v52_20261010','v53_20261010').replace('passed_actual49153_forward5_mature_CPU_native_e64_sources_own_training_queued_no_GPU_or_quality_completion_claimed','passed_actual_forward5_return_small32_wide2_GPU_restart_smallCPU_nine_parent_callbacks_compiled_full17848_QA89_sources_annual_training_running_no_quality_claim')
    text=text.replace('保存股票身份五日收益嵌入实际49153成熟样本CPU核对、原生64轮及独立解码来源；GPU验证训练和官方分数待实际完成','保存五日收益股票嵌入实际GPU重启和独立CPU验证，以及48项选优冻结完整推理QA89 main来源；年度训练和正式评分进行中')
    publisher=save('publish_forward5_restart_full178_sources_main_v53_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v64_20261010/native_launch.json'),'Replace exact childless observer64 with65 including full178, own forward5 independent full5 and 46 scoring cases; scientific workers unchanged')
    for name,p in [('actual_fast_optimization_progress_v65_20261010',observer),('actual_forward5_restart_full178_sources_main_v53_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'live65_started':True,'actual_restart_and_full178_sources_main53_started':True},flush=True)
if __name__=='__main__':main()
