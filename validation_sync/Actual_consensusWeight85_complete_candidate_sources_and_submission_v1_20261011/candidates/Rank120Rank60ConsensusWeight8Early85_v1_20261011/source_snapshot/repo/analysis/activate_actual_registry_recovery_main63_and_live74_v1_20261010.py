"""Show real latest registration handles and preserve failure/recovery evidence on main."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();proof=A/'Dual25_verified_recovery_exact_dependency_aliases_v4_20261010.json';routing=read(proof)
    tasks={};original_inverse={v:k for ver in (1,2) for k,v in read(A/f'Dual25_verified_recovery_exact_dependency_aliases_v{ver}_20261010.json')['driver_wrappers'].items()}
    for original in routing['selected_helpers']:
        name=routing['service_aliases'][original];definition=read(A/'service_owned_workflows_20261006'/original/'job_definition.json');driver=Path(definition['driver']).name;driver=original_inverse.get(driver,driver);tasks[name]=routing['driver_wrappers'][driver]
    records=[]
    for name,driver in tasks.items():
        folder=A/'service_owned_workflows_20261006'/name;l=read(folder/'native_launch.json');terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else {}
        if 'native42_and_after174_fast17_queue' in name:
            assert terminal['status']=='failed' and terminal['failure']=='AssertionError: '
            original42=A/'service_owned_workflows_20261006/actual_stock_top10_embedding_six_state_native42_v1_20261010';assert read(original42/'service_execution.json')['status']=='passed'
            fast=routing['service_aliases']['actual_stock_top10_embedding_after174_fast17_screen_v1_20261010'];assert owned(read(A/'service_owned_workflows_20261006'/fast/'native_launch.json'))
            records.append({'name':name,'status':'failed_original_parent_queue_retained_completed42_not_rerun_separate_actual17_worker_live','actual_native42_service':'actual_stock_top10_embedding_six_state_native42_v1_20261010','actual_fast17_service':fast});continue
        assert owned(l) or terminal.get('status')=='passed',(name,terminal);records.append({'name':name,'live_verified':owned(l),'terminal_status':terminal.get('status')})
    dispatch=A/'actual_registration_recovery_v4_dependency_handles_verified_v1_20261010.json';create(dispatch,{'status':'verified_all_unique_latest_dependency_handles_and_separate_existing_native42_fast17_parent_resume','records':records,'new_fits':0,'new_quality_scores':0,'no_completed42_repeated':True})
    text=(A/'monitor_fast_optimization_v73_20261010.py').read_text(encoding='utf8').replace('progress_v73','progress_v74').replace('handoff_v124','handoff_v125').replace('rankings_v45','rankings_v46')
    text=text.replace('Dual25_verified_recovery_exact_dependency_aliases_v1_20261010.json','Dual25_verified_recovery_exact_dependency_aliases_v4_20261010.json')
    jobs=list(dict.fromkeys([*routing['service_aliases'].values(),'StockRankDual174_full_registration_recovery_v3_20261010','StockRankDual174_verified_candidate_registration_recovery_v3_20261010','actual_registration_recovery_sources_main_v63_20261010']))
    text=text.replace('    while True:\n','    jobs += '+repr(jobs)+'\n    while True:\n')
    text=text.replace('        lines += [f"内存可用',"        lines.append(f\"174实际完整候选推理及封装已通过；登记恢复服务：{services['StockRankDual174_full_registration_recovery_v3_20261010']['status']}。原始失败及部分登记完整归档，原生42检查保留，新17项评分单独接续。\")\n        lines += [f\"内存可用")
    observer=save('monitor_fast_optimization_v74_20261010.py',text)
    paths=[Path(__file__),observer,proof,dispatch,A/'StockRankDual174_partial_registry_lossless_preservation_v1_20261010.json',A/'StockRankDual174_selected_release_v1_20261010/selected_candidate_ready_for_registration.json',A/'StockRankDual174_selected_release_v1_20261010/inference_ready.json',A/'recover_StockRankDual174_registry_folder_field_and_dependencies_v1_20261010.py',A/'resume_preserved_StockRankDual174_registration_v4_and_dependency_dispatch_v1_20261010.py',A/'dispatch_verified_empty_StockRankDual174_registration_and_dependencies_v4_20261010.py',A/'complete_remaining_verified_registry_dependency_dispatch_v4_20261010.py',*[Path(p) for p in routing['input_sha256']]]
    for job in ['StockRankDual174_selected_candidate_preparation_v1_20261010','StockRankDual174_selected_candidate_sealing_v1_20261010','StockRankDual174_round174_full_registration_v1_20261010','StockRankDual174_full_registration_recovery_v1_20261010']:
        f=A/'service_owned_workflows_20261006'/job;paths += [p for p in f.glob('*.json') if p.name in ('service_execution.json','native_launch.json','job_definition.json')]
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    source=A/'publish_StockRank20_full180_complete48_sources_main_v62_20261010.py';text=source.read_text(encoding='utf8');begin=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    text=text[:begin]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('StockRank20_full180_complete48_sources_v62','StockRankDual174_verified_candidate_registry_recovery_v63').replace('StockRank20_full180_complete48_sources_main_v62','StockRankDual174_verified_candidate_registry_recovery_main_v63').replace('StockRank20_full180_complete48_sources_main_receipt_v62','StockRankDual174_verified_candidate_registry_recovery_main_receipt_v63')
    text=text.replace('compiled_rank20_complete48_selected14_source_freeze_two_full_future_replays_QA91_and_main_routes_actual11_parent_callbacks_CPU_annual_training_pending','passed_actual174_complete_selected_inference_and_seal_preserved_partial_registry_folder_field_corrected_latest_actual_registration_v4_and_dependency_handles_verified_QA_main_pending')
    text=text.replace('保存二十日截面排名模型180轮完整48项比较、11个完整父方案回调、冻结推理与完整榜QA91源码；年度训练及质量评分按实际完成回执判定','保存174完整候选推理及封装通过证据、部分登记无损归档、folder字段与排他侧文件修复和实际依赖核验；完整榜QA85及main仍待完成，未重复训练推理评分')
    publisher=save('publish_StockRankDual174_actual_candidate_and_registry_recovery_main_v63_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v73_20261010/native_launch.json'),'Replace childless observer73 with74 showing verified actual registry4 recovery handles and original failures')
    for name,p in [('actual_fast_optimization_progress_v74_20261010',observer),('actual_registration_recovery_sources_main_v63_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'all_actual_dependencies_verified':True,'actual_registry_recovery_main63_queued':True,'live74_started':True},flush=True)
if __name__=='__main__':main()
