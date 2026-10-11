"""Publish actual mean20 maturity/restart evidence and observe all active validation jobs."""
from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();closed('StockForward20Embedding_actual_mature_fixture_CPU_v1_20261010');closed('actual_stock_forward20_embedding_small512_restart_v1_20261010')
    text=(A/'monitor_fast_optimization_v68_20261010.py').read_text(encoding='utf8').replace('progress_v68','progress_v69').replace('handoff_v119','handoff_v120').replace('rankings_v40','rankings_v41')
    jobs=['StockForward20Embedding_actual_mature_fixture_CPU_v1_20261010','actual_stock_forward20_embedding_own_training_queue_v1_20261010','actual_stock_forward20_embedding_small512_restart_v1_20261010','StockForward20EmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_forward20_embedding_small512_bank6_v1_20261010','StockForward20EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','actual_stock_forward20_embedding_six_state_native42_v1_20261010','actual_stock_forward20_embedding_full5_native42_and_early17_queue_v1_20261010','actual_stock_forward20_embedding_after173_fast17_screen_v1_20261010','actual_stock_forward20_embedding_after173_large_allocation29_screen_v1_20261010','actual_stock_forward20_embedding_after173_completion_main_v73_20261010','actual_stock_forward20_embedding_six_state_native42_completion_main_v74_20261010','actual_stock_forward20_embedding_after173_large29_completion_main_v75_20261010','actual_stock_forward20_embedding48_after178_normalization_queue_v5_20261010','StockForward20Embedding48_selected_native14_v5_20261010','StockForward20Embedding179_complete48_family_v6_20261010','actual_mean20_mature_GPU_sources_full179_main_v57_20261010']
    families=['StockForward20EmbeddingSmall512_after173_high_impact17_screen_v1_20261010','StockForward20EmbeddingSmall512_after173_large_allocation29_screen_v1_20261010']
    text=text.replace('    while True:\n','    jobs += '+repr(jobs)+'\n    families += '+repr(families)+'\n    while True:\n')
    text=text.replace('        state[\'screen_progress\']=summaries;',"        state['stock_forward20_embedding']={'completed_annual_models':[y for y in range(2020,2026) if Path(f'E:/赛题五_本机临时/stock_forward20_embedding_small512_BF16_bank6_v1_20261010/{y}/info.json').exists()],'bank_worker':services.get('actual_stock_forward20_embedding_small512_bank6_v1_20261010')}\n        state['screen_progress']=summaries;")
    text=text.replace('尚无官方评分结论。','17项和29项官方比较按实际分数回执更新。')
    text=text.replace('        lines += [f"内存可用',"        lines.append(f\"股票身份×120维特征×20日平均收益：年度模型{len(state['stock_forward20_embedding']['completed_annual_models'])}/6；48项完整资格服务{services['StockForward20Embedding179_complete48_family_v6_20261010']['status']}；新目标官方增益仍待实际评分。\")\n        lines += [f\"内存可用")
    observer=save('monitor_fast_optimization_v69_20261010.py',text)
    import admit_StockForward20Embedding179_complete48_pipeline_v2_20261010 as full
    paths=[Path(__file__),observer,*full.source_paths(),A/'stock_forward20_embedding179_full_execution_sources_admission_v2_20261010.json',A/'stock_forward20_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json',A/'stock_forward20_embedding_own64_native_sources_preparation_v1_20261010.json',A/'stock_forward20_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json']
    for proofname in ['stock_forward20_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json','stock_forward20_embedding_own64_native_sources_preparation_v1_20261010.json','stock_forward20_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json']:
        paths += [Path(p) for p in read(A/proofname)['input_sha256'] if Path(p).suffix in ('.json','.py')]
    for job in jobs[:4]:
        folder=A/'service_owned_workflows_20261006'/job
        paths += [p for p in folder.glob('*.json') if p.name in ('native_launch.json','service_execution.json','job_definition.json')]
    pointer=A/'actual_stock_forward20_embedding_mature_fixture_location_v1_20261010.json';paths += [pointer,Path(read(pointer)['output'])/'verification.json']
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    source=A/'publish_Top10_prospective_index_and175178_cascade_main_v56_20261010.py';text=source.read_text(encoding='utf8');begin=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    text=text[:begin]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('Top10_large29_prospective_index_and175178_routes','StockMean20_mature_GPU_sources_and179_routes').replace('v56_20261010','v57_20261010')
    text=text.replace('compiled_exact_Top10_large29_index_before_scoring_same47_31_48_48_and_full1753_1763_1774_1785_routes_no_scientific_restarts','passed_actual49153_mature_mean20_fixture_and_GPU32_wide2_restart_compiled48_QA90_sources_annual_training_and_quality_pending')
    text=text.replace('预防尚未开始的Top10大权重29项结果索引冲突，冻结的47/31/48/48项比较保持不变；175至178精确依赖和已验证推理缓存保留','保存股票身份与120维特征二十日收益目标的实际成熟49153样本和GPU重启检查，以及179轮48项验证源码；年度评分和未来推理尚待完成')
    publisher=save('publish_StockMean20_actual_mature_GPU_and179_sources_main_v57_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v68_20261010/native_launch.json'),'Replace verified childless observer68 with69; new mean20 actual jobs included; no scientific workers changed')
    for name,p in [('actual_fast_optimization_progress_v69_20261010',observer),('actual_mean20_mature_GPU_sources_full179_main_v57_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'live69_started':True,'actual_mean20_proofs_main57_started':True,'full179_quality_pending':True},flush=True)
if __name__=='__main__':main()
