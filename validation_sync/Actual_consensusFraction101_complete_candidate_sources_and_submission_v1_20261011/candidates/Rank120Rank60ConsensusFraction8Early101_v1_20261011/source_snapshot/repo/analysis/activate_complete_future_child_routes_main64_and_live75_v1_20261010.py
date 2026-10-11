"""Publish exact future-child routing and observe all actual current native handles."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();proof=A/'Dual25_verified_recovery_exact_dependency_aliases_v5_20261010.json';routing=read(proof)
    actual=[]
    for n in routing['selected_helpers']:
        name=routing['service_aliases'][n];folder=A/'service_owned_workflows_20261006'/name;launch=read(folder/'native_launch.json');terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else {}
        assert owned(launch) or terminal.get('status')=='passed',(name,terminal);actual.append({'original':n,'actual_service':name,'live_verified':owned(launch),'terminal':terminal.get('status')})
    check=A/'actual_complete_future_child_routes_and_pending_native_handles_v5_20261010.json';create(check,{'status':'verified_current_native_handles_all_unstarted_child_types_pinned_before_future_dispatch','records':actual,'registered174_worker_preserved':True,'input_sha256':{str(proof):sha(proof)},'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    text=(A/'monitor_fast_optimization_v74_20261010.py').read_text(encoding='utf8').replace('progress_v74','progress_v75').replace('handoff_v125','handoff_v126').replace('rankings_v46','rankings_v47')
    text=text.replace('Dual25_verified_recovery_exact_dependency_aliases_v4_20261010.json','Dual25_verified_recovery_exact_dependency_aliases_v5_20261010.json')
    text=text.replace('    while True:\n','    jobs += '+repr(list(dict.fromkeys([*routing['service_aliases'].values(),'actual_complete_future_child_routes_main_v64_20261010'])))+'\n    while True:\n')
    observer=save('monitor_fast_optimization_v75_20261010.py',text)
    paths=[Path(__file__),observer,proof,check,A/'prepare_complete_future_child_routing_and_pending_dependencies_v5_20261010.py',*[Path(p) for p in routing['input_sha256']]]
    source=A/'publish_StockRankDual174_actual_candidate_and_registry_recovery_main_v63_20261010.py';text=source.read_text(encoding='utf8');begin=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    text=text[:begin]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
    text=text.replace('StockRankDual174_verified_candidate_registry_recovery_v63','Complete_future_child_routes_v64').replace('StockRankDual174_verified_candidate_registry_recovery_main_v63','Complete_future_child_routes_main_v64').replace('StockRankDual174_verified_candidate_registry_recovery_main_receipt_v63','Complete_future_child_routes_main_receipt_v64')
    text=text.replace('passed_actual174_complete_selected_inference_and_seal_preserved_partial_registry_folder_field_corrected_latest_actual_registration_v4_and_dependency_handles_verified_QA_main_pending','verified_actual_current_dependency_handles_and_all15_unstarted_child_entry_types_including_cache_selected_candidate_own_closed_routes_before_future_dispatch_existing174_registry_preserved')
    text=text.replace('保存174完整候选推理及封装通过证据、部分登记无损归档、folder字段与排他侧文件修复和实际依赖核验；完整榜QA85及main仍待完成，未重复训练推理评分','保存待执行流程15类封装与完整登记子入口、缓存嵌套候选的显式依赖、22个真实等待任务核验；174正在登记且未重启，科学控制和模型数学不变')
    publisher=save('publish_complete_future_child_routes_main_v64_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v74_20261010/native_launch.json'),'Replace childless observer74 with75 showing actual complete future child routing and current handles')
    for name,p in [('actual_fast_optimization_progress_v75_20261010',observer),('actual_complete_future_child_routes_main_v64_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'all_future_children_current_handles_verified':True,'main64_queued':True,'live75_started':True},flush=True)
if __name__=='__main__':main()
