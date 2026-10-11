"""Publish completed prospective controls and failed identities after full115 closes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    source=A/'publish_protected_upper_pool_HGB66_candidate_pipeline_20261007.py'
    target=A/'publish_HGB88_complete_pipeline_20261007.py';assert not target.exists()
    text=source.read_text(encoding='utf8')
    text=text.replace('protected_upper_pool_HGB66_candidate_pipeline_github_20261007','HGB88_complete_pipeline_github_20261007')
    text=text.replace("closed('local_closed_dependency_recovery_v2_main_publication')","closed('protected_upper_pool_HGB66_round115_full_registration_v5')")
    text=text.replace("closed('cpu_full_universe_ElasticNet24_bank_evidence_publication_v4')","closed('local_only_progress_monitor_v12_handoff')")
    text=text.replace('protected_upper_pool_HGB66_candidate_source_admission_20261007.json','flagged_HGB88_round116_source_admission_20261007.json')
    text=text.replace('passed_actual_native_hook_and24_prospective_source_AST_hashes_schema_and_parent_baseline_controls','passed_actual85_full_controls_and24_prospective116_source_schema_baseline_and_ablation_routes')
    start=text.index('    sources=[Path(__file__),proof_path');end=text.index('    pins={str(p):sha(p)',start)
    replacement="""    prepared=read(A/'flagged_HGB88_complete_pipeline_preparation_v4_20261007.json')
    sources=[Path(__file__),A/'prepare_HGB88_complete_pipeline_main_publication_20261007.py',proof_path,*map(Path,proof['input_sha256']),*map(Path,prepared['input_sha256']),
        A/'flagged_HGB88_complete_pipeline_preparation_v4_20261007.json',A/'flagged_HGB88_complete_pipeline_actual_hidden_launches_v4_20261007.json',
        A/'prepare_flagged_HGB88_pipeline_complete_v4_20261007.py',A/'prepare_local_monitor12_and_HGB88_launch_20261007.py',
        A/'monitor_local_only_runtime_v12_20261007.py',A/'handoff_local_only_monitor_v12_20261007.py',
        *list((A/'local_only_monitor_v12_actual_handoff_20261007').glob('*.json')),
        A/'flagged_HGB_small_amplitude88_controls_github_20261007/receipt.json',
        A/'CPU_full_bank_resource_observer_ElasticNet_v4_github_20261007/receipt.json',
        A/'github_validation_sync_main_20261005/round115_receipt.json',
        A/'optimization_20261003_r115/full_registration_execution.json',A/'optimization_20261003_r115/provenance_scope_execution.json',
        *list(A.glob('protected_upper_pool_HGB66_round115*recovery*20261007.json')),
        A/'protected_upper_pool_HGB66_round115_inherited_registry_alias_relocation_20261007.json',
        A/'local115_alias_and116_dependency_recovery_admission_20261007.json',A/'local115_alias_and116_dependency_recovery_actual_hidden_launches_20261007.json',
        A/'flagged_HGB88_dependency_routes_v3_admission_20261007.json',
        A/'flagged_HGB88_round116_pipeline_preparation_prototype_failure_20261007.json']
    names=[job['name'] for job in prepared['jobs']]+['protected_upper_pool_HGB66_round115_full_registration',
        'protected_upper_pool_HGB66_round115_full_registration_v2','protected_upper_pool_HGB66_round115_full_registration_v3',
        'protected_upper_pool_HGB66_round115_full_registration_v4','protected_upper_pool_HGB66_round115_full_registration_v5',
        'flagged_HGB_small_amplitude88_official_comparison','flagged_HGB_small_amplitude88_official_comparison_v2','flagged_HGB_small_amplitude88_official_comparison_v3',
        'flagged_HGB_small_amplitude88_selected_candidate_preparation','flagged_HGB_small_amplitude88_selected_candidate_sealing',
        'flagged_HGB_small_amplitude88_scores_main_publication']
    for name in names:
        folder=A/'service_owned_workflows_20261006'/name
        sources += [folder/n for n in ('job_definition.json','native_launch.json')]
        if not owned(read(folder/'native_launch.json')):sources += list(folder.glob('*.json'))+list(folder.glob('*.log'))
"""
    text=text[:start]+replacement+text[end:]
    text=text.replace('validation_sync/protected_upper_pool_HGB66_candidate_pipeline_20261007','validation_sync/HGB88_complete_pipeline_20261007')
    text=text.replace('published_actual_native_hook_and_prospective_full115_pipeline_controls','published_actual85_full_controls_and_prospective_full116_pipeline_with_failed_dependency_history')
    text=text.replace("'actual_historical_native_hook_cases':63","'actual_full5635800_transform_controls':85").replace('canonical115_sources_written_by_admission','canonical116_sources_written_by_admission')
    text=text.replace('future_full115_qualification_not_claimed','future_full116_qualification_not_claimed').replace('future66_scores_and_full115_QA26_not_claimed_complete','future88_scores_and_full116_QA27_not_claimed_complete')
    start=text.index("            payload[(prefix/'README.md').as_posix()]=(");end=text.index('            scope.reverify()',start)
    replacement="""            payload[(prefix/'README.md').as_posix()]=('# 本机HGB小权重完整流程和实际故障恢复记录\\n\\n'
                '85项方案已通过完整5635800行独立变换与255个冷前缀控制；下一轮88项官方评分等待115完整QA26及main完成后运行。'
                '本目录保存24份未来登记源码的编译与摘要、9项比较基准增益元数据控制、移除涨停分支及保留非涨停分支图结构控制。'
                '复用已有20模型，比较基准和兼容方案基底分别记录，不新增训练。'
                '同时保留历史登记路径冲突、依赖退出的真实状态及隐藏启动身份，115原始66项分数及原冻结不重写。'
                '未来选中方案仍须封存、完整推理或精确锚点复用、完整QA27及main上传；本次不宣称这些已完成。\\n').encode('utf8')
"""
    text=text[:start]+replacement+text[end:]
    text=text.replace('登记低分区HGB候选冻结封存及完整115流程的24源码9项基准回归','登记本机HGB小权重完整116流程与真实依赖恢复记录')
    compile(text,str(target),'exec')
    with target.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    pins={str(p):sha(p) for p in (Path(__file__),source,target,A/'flagged_HGB88_round116_source_admission_20261007.json')}
    row=start_service('HGB88_complete_pipeline_main_publication',target.name,[],pins)
    create(A/'HGB88_complete_pipeline_main_publication_actual_launch_20261007.json',{'input_sha256':pins,'actual_native_launch':row,'new_quality_scores':0})
    print({'status':'launched_pipeline_publication','pid':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
