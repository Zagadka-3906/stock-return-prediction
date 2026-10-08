"""Prepare a serialized main handoff after136 qualification, preserving every failed/actual pending receiver."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    old=A/'publish_completed144_and_full_recovery_lineage_v21_20261008.py';text=old.read_text(encoding='utf8').replace('v21','v22')
    text=text.replace('def main():','def publish_once():',1)
    text=text.replace('from monitor_actual135_144_connected_API_progress_v20_20261008 import snapshot','from monitor_actual_chronological_optimization_progress_v22_20261008 import snapshot')
    text=text.replace("progress=snapshot();assert progress['best_fully_qualified_round']==144", "progress=snapshot();progress['best_fully_qualified_round']=progress['best_fully_qualified']['round'];progress['best_fully_qualified_score']=progress['best_fully_qualified']['score'];assert progress['best_fully_qualified_round']==136")
    text=text.replace('datetime.datetime(2026,10,8,14,50)','datetime.datetime(2026,10,8,16,0)')
    text=text.replace("A/'latest_verified_submission_delivery_v1_20261008.json'", "A/'latest_verified_submission_delivery_v2_20261008.json'")
    needle="delivery=Path(read(A/'latest_verified_submission_delivery_v2_20261008.json')['output']);sources.extend([delivery/'submission_manifest.json',delivery/'提交说明.md'])"
    assert text.count(needle)==1
    text=text.replace(needle,needle+"\n    sources.extend([A/'github_validation_sync_main_20261005/round136_receipt.json',A/'optimization_20261003_r136/full_registration_execution.json',A/'pending137to141_collector_controls_v14_20261008.json',A/'pending137to141_receiver_dispatch_v14_20261008.json',A/'pending14_idle_publication_hold_for_handoff22_20261008.json'])")
    text=text.replace("'best_fully_qualified_round':144", "'best_fully_qualified_round':136")
    text=text.replace('actual140_completed_scores_two_full_qualified_rounds_new_best144_ready_E_delivery_and_all_recovery_lineage_snapshot','actual234_completed_scores_new_best136_fully_qualified_and_pending14_all_recovery_lineage_snapshot')
    text=text.replace("'actual13694_quality_running_not_claimed_complete':True", "'actual13694_quality_and_full_native_QA47_main_completed':True,'pending137_to141_308_cases_remain':True")
    left=text.index("    payload[(prefix/'README.md').as_posix()]='''");right=text.index("'''.encode('utf8')",left)+len("'''.encode('utf8')")
    text=text[:left]+"""    payload[(prefix/'README.md').as_posix()]='''# 第136轮完成及后续五轮实际恢复

第136轮94项原始官方连续前向评分已完成，最高S=0.4511623376562006。22个物理模型的两次完整1599600行原生推理、独立解码、保存重载、CSV逐字节复现及冷80天均已通过。源码、方案、参数及TRAIN成熟收益映射在未来特征读取之前冻结。完整榜13972项，原始六视图45秒QA47及main同步已完成。

后续137至141轮的120份预生成程序及全部方案图、字段、排序、模型去重、D/E文件检查通过。旧13接收流程因136旧登记路径错误失败，原始错误及文件均保留。新14流程在实际136完整main证明后启动，使用实际D1元数据的15版前检，不把失败14前检改记为成功。五轮预定308项评分仍待实际执行。

另准备了125项较小幅度及较细混合比例的可行方案草案，复用四个既有残差模型头；草案尚未获准评分，也未执行新推理。现有最优落在原网格最小正幅度，因此尚不能宣称方向或资源穷尽。

截止：10月10日23:59。E盘最新完全合格提交CSV及校验清单已经准备；旧144轮文件保留。未向比赛平台执行提交，未读取实际测试标签。同步时只临时挂起仍在等待依赖的Git发布接收程序，不停止模型验证进程；全部通过、失败和运行中状态分别保留。
'''.encode('utf8')"""+text[right:]
    before="if __name__=='__main__':main()";assert text.count(before)==1
    wrapper="""def main():
    gate=A/'service_owned_workflows_20261006/CrossFamily94_round136_full_registration_v6_20261008'
    while not (gate/'native_launch.json').exists() or owned(read(gate/'native_launch.json')):time.sleep(10)
    assert read(gate/'service_execution.json')['status']=='passed'
    dispatch=A/'pending137to141_receiver_dispatch_v14_20261008.json'
    while not dispatch.exists():time.sleep(2)
    assert read(dispatch)['status']=='passed_all41_fresh_chronological_receivers_dispatched_after120_prospective_sources'
    from maintain_best_fully_qualified_submission_delivery_v2_20261008 import update
    pointer=A/'latest_verified_submission_delivery_v2_20261008.json'
    while not pointer.exists() or read(pointer)['selected_round']!=136:time.sleep(2)
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    row=read(A/'service_owned_workflows_20261006/Huber52_controls_main_publication_v14_20261008/native_launch.json');held=[]
    try:
        assert owned(row)
        parent,worker,proof=suspended_idle(row,'    closed (publish_Huber52_evidence_v14_20261008.py:')
        held.extend((worker,parent))
        create(A/'pending14_idle_publication_hold_for_handoff22_20261008.json',{
            'status':'held_only_owned_waiting_publication_receiver_before_any_Git_mutation',
            'identity':row,'actual_idle_stack_before_and_after':proof,'scientific_workers_stopped':0,
            'resume_required_in_finally':True})
        publish_once()
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()

if __name__=='__main__':main()"""
    text=text.replace(before,wrapper)
    target=A/'publish_completed136_and_full_recovery_lineage_v22_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'actual136_pending14_handoff22_source_preparation_20261008.json',{
        'status':'prepared_serialized_main_handoff_after_actual1366_complete_qualification_and_pending14_dispatch',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target]},'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('completed136_and_full_recovery_lineage_main_v22_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),target]})
    create(A/'completed136_and_full_recovery_lineage_main_v22_hidden_launch_20261008.json',row)
    print({'service':row['name'],'worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
