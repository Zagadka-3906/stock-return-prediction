"""Observe explicit recovery aliases and publish the immutable routing proof on main."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();closed('actual_stock_dual_embedding_after173_verified_recovery_completion_main_v76_20261010')
    proof=A/'Dual25_verified_recovery_exact_dependency_aliases_v1_20261010.json';routing=read(proof)
    text=(A/'monitor_fast_optimization_v69_20261010.py').read_text(encoding='utf8').replace('progress_v69','progress_v70').replace('handoff_v120','handoff_v121').replace('rankings_v41','rankings_v42')
    text=text.replace('    while True:\n','    jobs += '+repr(list(routing['service_aliases'].values())+['actual_Dual25_recovery_dependencies_main_v58_20261010'])+'\n    while True:\n')
    needle="        state={'at_local':";position=text.index(needle)
    injected="        original_services=dict(services)\n        alias_proof=read(A/'Dual25_verified_recovery_exact_dependency_aliases_v1_20261010.json')\n        for original,actual in alias_proof['service_aliases'].items():\n            services[original]={**services.get(actual,{'status':'not_started'}),'actual_service_alias':actual,'original_service_status':original_services.get(original,{}).get('status'),'explicit_recovery_routing_not_original_terminal_status':True}\n"
    text=text[:position]+injected+text[position:]
    text=text.replace("        state['stock_embedding_completed_models']", "        state['original_service_states_before_explicit_aliases']=original_services\n        state['stock_embedding_completed_models']")
    observer=save('monitor_fast_optimization_v70_20261010.py',text)
    paths=[Path(__file__),observer,proof,A/'stock_dual_embedding_actual25_terminal_pointer_recovery_v1_20261010.json',A/'stock_dual_embedding25_after173_completion_main_receipt_v57_20261010.json',*[Path(p) for p in routing['input_sha256']]]
    for job in ['actual_Dual25_verified_terminal_recovery_v1_20261010','actual_stock_dual_embedding_after173_high_impact25_screen_v1_20261010','actual_stock_dual_embedding_after173_verified_recovery_completion_main_v76_20261010']:
        folder=A/'service_owned_workflows_20261006'/job;paths += [p for p in folder.glob('*.json') if p.name in ('native_launch.json','service_execution.json','job_definition.json')]
    source=A/'publish_StockMean20_actual_mature_GPU_and179_sources_main_v57_20261010.py';text=source.read_text(encoding='utf8');begin=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    text=text[:begin]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
    text=text.replace('StockMean20_mature_GPU_sources_and179_routes','Dual25_verified_recovery_exact_dependencies').replace('v57_20261010','v58_20261010')
    text=text.replace('passed_actual49153_mature_mean20_fixture_and_GPU32_wide2_restart_compiled48_QA90_sources_annual_training_and_quality_pending','passed_actual25_scores24_full72_prefix_terminal_recovery_published_main_explicit_dependency_aliases_original_failures_retained')
    text=text.replace('保存股票身份与120维特征二十日收益目标的实际成熟49153样本和GPU重启检查，以及179轮48项验证源码；年度评分和未来推理尚待完成','保存实际25项双目标融合的终端索引恢复及显式后续依赖；原失败记录保留，44至48项科学方案和全部模型检查不变，未重复评分')
    publisher=save('publish_Dual25_verified_recovery_dependencies_main_v58_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v69_20261010/native_launch.json'),'Replace childless observer69 with70 showing explicit recovery aliases and retaining original statuses')
    for name,p in [('actual_fast_optimization_progress_v70_20261010',observer),('actual_Dual25_recovery_dependencies_main_v58_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'live70_started':True,'verified_Dual25_dependencies_main58_started':True},flush=True)
if __name__=='__main__':main()
