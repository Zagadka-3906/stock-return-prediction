"""Publish real mean20 rank population controls; observe pending rank20 GPU fits honestly."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();closed('StockRank20Embedding_actual_mature_fixture_CPU_v1_20261010')
    text=(A/'monitor_fast_optimization_v71_20261010.py').read_text(encoding='utf8').replace('progress_v71','progress_v72').replace('handoff_v122','handoff_v123').replace('rankings_v43','rankings_v44')
    jobs=['StockRank20Embedding_actual_mature_fixture_CPU_v1_20261010','actual_stock_rank20_embedding_own_training_queue_v1_20261010','actual_stock_rank20_embedding_small512_restart_v1_20261010','StockRank20EmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_rank20_embedding_small512_bank6_v1_20261010','actual_StockMean20_own6_full5_main_v60_20261010','actual_rank20_real49153_CPU7_own64_sources_main_v61_20261010']
    text=text.replace('    while True:\n','    jobs += '+repr(jobs)+'\n    while True:\n')
    needle="        state['screen_progress']=summaries;";assert text.count(needle)==1
    text=text.replace(needle,"        state['stock_rank20_embedding']={'completed_annual_models':[y for y in range(2020,2026) if Path(f'E:/赛题五_本机临时/stock_rank20_embedding_small512_BF16_bank6_v1_20261010/{y}/info.json').exists()],'own_queue':services.get('actual_stock_rank20_embedding_own_training_queue_v1_20261010'),'GPU_queue_waits_actual174_candidate_seal':True}\n"+needle)
    text=text.replace('        lines += [f"内存可用',"        lines.append(f\"股票身份×20日截面排名：真实49153成熟样本和全成熟日Pandas排名验证完成；年度模型{len(state['stock_rank20_embedding']['completed_annual_models'])}/6；GPU训练优先等待174候选封装。\")\n        lines += [f\"内存可用")
    observer=save('monitor_fast_optimization_v72_20261010.py',text)
    prep=A/'stock_rank20_embedding_own64_native_sources_preparation_v1_20261010.json';admission=A/'stock_rank20_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json';pointer=A/'actual_stock_rank20_embedding_mature_fixture_location_v1_20261010.json'
    fixture=Path(read(pointer)['output']);paths=[Path(__file__),observer,prep,admission,pointer,fixture/'verification.json',A/'recent252_rank20_mature_population_actual_CPU_controls_v1_20261010.json',A/'run_stock_rank20_embedding_own_training_queue_v1_20261010.py']
    for p in [*read(prep)['input_sha256'],*read(admission)['input_sha256']]:
        path=Path(p)
        if path.suffix in ('.py','.json'):paths.append(path)
    for job in jobs[:2]:
        folder=A/'service_owned_workflows_20261006'/job;paths += [p for p in folder.glob('*.json') if p.name in ('native_launch.json','service_execution.json','job_definition.json')]
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    source=A/'publish_StockMean20_actual_own6_full5_main_v60_20261010.py';text=source.read_text(encoding='utf8');begin=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    text=text[:begin]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('StockMean20_actual_own6_full5_v60','StockRank20_real49153_CPU7_own64_sources_v61').replace('StockMean20_actual_own6_full5_main_v60','StockRank20_real49153_CPU7_own64_sources_main_v61').replace('StockMean20_actual_own6_full5_main_receipt_v60','StockRank20_real49153_CPU7_own64_sources_main_receipt_v61')
    text=text.replace('passed_actual6_own64_mature_mean20_identity_cross120_models_and_complete5635800_independent_native_replays_with10_cold_prefixes_quality_pending','passed_actual49153_rank20_identity_cross120_mature_fixture_and_all_mature_day_Pandas_rank_bits_and7_scalar_poison_cases_own64_GPU_training_pending')
    text=text.replace('保存股票身份与120维特征二十日收益目标的实际六年度64轮成熟训练、5635800行独立重放及10个冷启动前缀；官方质量评分仍待完成','保存股票身份与120维特征二十日截面排名目标的实际49153成熟样本、全成熟日Pandas排名位级检查和7项标量因果检查；年度GPU训练等待174候选封装')
    publisher=save('publish_StockRank20_actual49153_CPU7_own64_sources_main_v61_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v71_20261010/native_launch.json'),'Replace childless observer71 with72 including actual rank20 fixture and deferred GPU queue')
    for name,p in [('actual_fast_optimization_progress_v72_20261010',observer),('actual_rank20_real49153_CPU7_own64_sources_main_v61_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'actual_rank20_maturity_proofs_main61_started':True,'live72_started':True,'GPU_training_not_claimed_complete':True},flush=True)
if __name__=='__main__':main()
