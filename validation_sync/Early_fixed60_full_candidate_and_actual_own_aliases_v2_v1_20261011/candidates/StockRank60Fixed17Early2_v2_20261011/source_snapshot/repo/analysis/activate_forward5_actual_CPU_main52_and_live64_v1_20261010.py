"""Record actual forward5 fixture validation on main and retain live queue visibility."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    source=A/'monitor_fast_optimization_v63_20261010.py';text=source.read_text(encoding='utf8').replace('progress_v63','progress_v64').replace('handoff_v109','handoff_v111').replace('rankings_v35','rankings_v36')
    needle='    while True:\n';assert text.count(needle)==1
    jobs=['StockForward5Embedding_actual_mature_fixture_CPU_v1_20261010','actual_stock_forward5_embedding_own_training_queue_v1_20261010','actual_stock_forward5_embedding_small512_restart_v1_20261010','StockForward5EmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_forward5_embedding_small512_bank6_v1_20261010','actual_forward5_actual_CPU_sources_main_v52_20261010']
    text=text.replace(needle,'    jobs += '+repr(jobs)+'\n'+needle)
    needle="        state['screen_progress']=summaries";assert text.count(needle)==1
    text=text.replace(needle,"        state['stock_forward5_embedding']={'completed_annual_models':[y for y in range(2020,2026) if Path(f'E:/赛题五_本机临时/stock_forward5_embedding_small512_BF16_bank6_v1_20261010/{y}/info.json').exists()], 'bank_worker':services.get('actual_stock_forward5_embedding_small512_bank6_v1_20261010'),'actual_mature_fixture':services.get('StockForward5Embedding_actual_mature_fixture_CPU_v1_20261010')}\n"+needle)
    needle='        lines += [f"内存可用';assert text.count(needle)==1
    text=text.replace(needle,"        lines.append(f\"股票身份×五日平均收益：成熟49153样本实际验证通过；已完成年度训练{len(state['stock_forward5_embedding']['completed_annual_models'])}/6，GPU重启与独立推理按实际回执判定。尚无官方评分结论。\")\n"+needle)
    observer=save('monitor_fast_optimization_v64_20261010.py',text)
    source=A/'publish_Rank5_complete48_sources_actual_main_v51_20261010.py';text=source.read_text(encoding='utf8');start=text.index('    paths=[');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    names=['prepare_stock_forward5_embedding_own64_native_and_fixture_v1_20261010.py','stock_forward5_embedding_small512_BF16_native_v1_20261010.py','stock_forward5_embedding_saved_tensor_decoder_v1_20261010.py','stock_forward5_embedding_own64_native_sources_preparation_v1_20261010.json','verify_stock_forward5_embedding_actual_mature_fixture_v1_20261010.py','actual_stock_forward5_embedding_mature_fixture_location_v1_20261010.json','admit_stock_forward5_embedding_actual_restart_and_own6_v1_20261010.py','stock_forward5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json','verify_stock_forward5_embedding_small512_restart_v1_20261010.py','verify_stock_forward5_embedding_small512_small_CPU_v1_20261010.py','train_stock_forward5_embedding_small512_BF16_bank6_own64_v1_20261010.py','run_stock_forward5_embedding_own_training_queue_v1_20261010.py','monitor_fast_optimization_v64_20261010.py',Path(__file__).name]
    fixture=Path(read(A/'actual_stock_forward5_embedding_mature_fixture_location_v1_20261010.json')['output'])
    names=[str(A/n) for n in names]+[str(p) for p in fixture.glob('*.json')];assert all(Path(p).is_file() for p in names)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr(names)+']]\n'+text[end:]
    text=text.replace('StockRank5Embedding_complete48_sources','StockForward5Embedding_actual_mature_CPU_sources').replace('v51_20261010','v52_20261010').replace('compiled_rank5_e64_complete48_normalizer_selected14_candidate_freeze_two_replay_registry_QA88_main_sources_actual17_and29_scoring_pending','passed_actual49153_forward5_mature_CPU_native_e64_sources_own_training_queued_no_GPU_or_quality_completion_claimed').replace('rank5_quality_improvement_not_yet_established','forward5_quality_improvement_not_yet_established')
    text=text.replace('保存股票身份五日排名64轮模型的48项选优、14原生因果检查、冻结后两次完整推理、QA88及main来源；分数与未来候选待实际验证','保存股票身份五日收益嵌入实际49153成熟样本CPU核对、原生64轮及独立解码来源；GPU验证训练和官方分数待实际完成')
    publisher=save('publish_forward5_actual_CPU_sources_main_v52_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v63_20261010/native_launch.json'),'Supersede exact childless observer63 with64 to include actual new forward5-return fixture and own training queue; scientific workers unchanged')
    for name,p in [('actual_fast_optimization_progress_v64_20261010',observer),('actual_forward5_actual_CPU_sources_main_v52_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'live64_started':True,'actual_forward5_CPU_main52_publication_started':True},flush=True)
if __name__=='__main__':main()
