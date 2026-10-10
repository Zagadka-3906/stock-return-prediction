"""Complete interrupted helper dispatch only; publish passed29 under its real terminal service identity."""
from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();proofpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json';proof=read(proofpath)
    actual='actual_stock_top10_embedding_after174_large_allocation29_screen_v2_after_Dual25_recovery_v1_dispatch_v4_future_children_v5_20261010'
    source=A/'publish_stock_top10_embedding_after174_large_allocation29_completion_v72_20261010.py';publisher=A/'publish_stock_top10_embedding_after174_large_allocation29_completion_v80_20261010.py'
    text=source.read_text(encoding='utf8').replace('actual_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010',actual)
    needle='    paths.extend(service/name';assert text.count(needle)==1
    text=text.replace(needle,"    paths += [A/'recover_all_actual_terminal_dependency_routes_v6_20261010.py',A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json',A/'all_actual_terminal_dependency_routes_endpoint_audit_v6_20261010.json',Path(__file__)]\n"+needle)
    text=text.replace('保存新股票身份嵌入模型六年度训练独立检查和17项真实TRAIN官方评分、16项完整及48项因果前缀控制','保存实际Top10身份模型29项TRAIN官方评分、28项完整与84项因果前缀控制；对应实际已通过的终端服务身份')
    assert not publisher.exists();compile(text,str(publisher),'exec');publisher.write_text(text,encoding='utf8',newline='\n')
    name='actual_stock_top10_embedding_after174_large_allocation29_completion_main_v80_20261010'
    assert allowed();row=start_service(name,publisher.name,[],{str(publisher):sha(publisher),str(proofpath):sha(proofpath)});create(A/(name+'_activation.json'),row)
    receipts=[]
    for item in proof['selected_helpers']:
        folder=A/'service_owned_workflows_20261006'/item['new']
        if folder.exists():
            terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
            assert terminal is not None or owned(read(folder/'native_launch.json')),item['new']
            receipts.append({'name':item['new'],'status':terminal['status'] if terminal else 'verified_owned_live','restarted':False});continue
        definition=read(A/'service_owned_workflows_20261006'/item['old']/'job_definition.json');original=Path(definition['driver']).name;driver=proof['driver_wrappers'].get(original,original);assert driver!=original
        assert allowed();row=start_service(item['new'],driver,definition['arguments'],{str(A/driver):sha(A/driver),str(proofpath):sha(proofpath)});create(A/(item['new']+'_activation.json'),row)
        receipts.append({'name':item['new'],'status':'dispatched_missing_exclusive_helper_only','restarted':False})
    create(A/'all_actual_terminal_routes6_resumed_missing_dispatch_and_actual_Top29_identity_v1_20261010.json',{'status':'completed_only_missing_exclusive_helper_dispatch_and_actual_passed_screen_metadata_publisher','records':receipts,'actual_Top29_publisher':name,'actual_passed_screen':actual,'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,publisher,proofpath]},'original_failed_publisher_preserved':True,'new_model_fits':0,'new_quality_scores':0,'scientific_workers_restarted':0})
    print({'actual_helpers':len(receipts),'actual_Top29_publisher':name,'scientific_workers_restarted':0},flush=True)
if __name__=='__main__':main()
