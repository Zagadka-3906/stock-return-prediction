"""Record seven implemented complete queues and completed141 correctness controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    previous=A/'actual_optimization_handoff_v12_20261008.json';state=read(previous)
    progress=read(A/'actual_optimization135_to141_progress_v10_20261008.json');assert progress['observer_version']==10
    routes=A/'KrylovGram52_prospective_routes_v2_20261008.json';proof=read(routes)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==1029 and proof['actual_physical_model_count_controls']==8
    assert len(proof['baseline_controls'])==9 and len(proof['same_score_sort_controls'])==6
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    launches_path=A/'KrylovGram141_complete_hidden_launches_v2_20261008.json'
    files=[Path(__file__),previous,routes,launches_path,A/'KrylovGram141_complete_dependency_plan_v2_20261008.json',
        A/'KrylovGram141_receiver_preparation_v2_20261008.json',A/'KrylovGram141_parent_set_recovery_v2_20261008.json',
        A/'KrylovGram141_prospective_QA_literal_recovery_v2_20261008.json',A/'KrylovGram141_historical_causal_main_v1_20261008/receipt.json',
        A/'KrylovGram141_archive_and_observer_preparation_v1_20261008.json',A/'actual_KrylovGram141_completed_CSV_archivist_hidden_launch_v1_20261008.json',
        A/'actual_optimization135_to141_progress_hidden_launch_v10_20261008.json',A/'monitor_actual_optimization135_to141_v10_20261008.py',
        A/'archive_KrylovGram141_completed_scoring_CSV_v1_20261008.py']
    services=state['actual_owned_live_services']
    for name,row in read(launches_path)['launches'].items():
        assert owned(row) and row['actual_native_console_handle']==0,name
        services[name]={'round':141,'identity':row,'live':True};folder=A/'service_owned_workflows_20261006'/name
        files += [folder/'native_launch.json',folder/'job_definition.json']
    for name,item in services.items():assert owned(item['identity']),name
    state.update(status='active_seven_complete135_to141_queues_with_completed141_controls_and_source_admission',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),actual_progress_at_checkpoint=progress,actual_owned_live_services=services,
        input_sha256={**state['input_sha256'],**{str(p):sha(p) for p in files}},
        actual141_complete_quality_pipeline_not_yet_prepared=False,actual141_complete_quality_pipeline_prepared=True,
        actual141_controls=progress['actual141_completed_preliminary_controls'],actual141_quality=progress['actual141_quality'],
        still_required141=['Complete140 registration3 QA51/main; exact qualified138139140 parent and49full147cold current-parent checks.',
            'All52 original official full8 metric comparisons; publish completed current control and score evidence to main.',
            'Freeze selected whole graph, calibration, model/config/source bytes before actual future X.',
            'Two full1599600 native/independent replays and cold80, or honest exact qualified anchor reuse with zero new inference.',
            'Unique physical modelSHA union, all six complete leaderboard views,45second QA52 and verified remote main receipt.'],
        actual141_launch_metadata={'round':141,'expected_official_cases':52,'QA_version':52,'science_receivers':2,
            'native_numerical_recipe':2,'bank_administration':3,'eligible_parents':[138,139,140],'old_failed_sources_preserved':True})
    create(A/'actual_optimization_handoff_v13_20261008.json',state)
    best=progress['best_fully_qualified'];epoch=progress['latest_actual_epoch']
    lines=['# 实际优化交接 v13','',f"记录时间：{state['at_local']}；截止：2026年10月10日23:59（UTC+8）。",'',
        f"完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；神经年度完成{len(progress['annual_models_complete'])}/6，{epoch['year']}年度完成{epoch['completed_epoch']}/{epoch['total_epochs']}轮、保存{epoch['saved_epoch']}轮。",'',
        '135–141七轮完整队列已实施并运行或等待已验证依赖。原GPU训练未停止或重启。',
        '第141轮20成熟年度模型/4完整OOF、5窗口/20实际标签扰动重训练、49完整/147冷、24历史原生/24冷、24跨年/48按日及7接入检查均已通过并同步main。',
        '24接收器/1029完整父图/9基准/6同分/8物理SHA计数和9原官方D评分目录范围检查通过；源版本2修复父方案编号及QA比较字符串，旧版保留。',
        '八步骤队列等待完整140注册版本3、QA51、main后继续52官方评分、冻结、实际候选、QA52和完整榜main。尚未完成的质量分或候选不计入完成。',
        '实时进度：actual_optimization135_to141_progress_v10_20261008.md。大文件均在E，原评分目录在D。',
        '目标active，没有全局可行方向或计算资源边界证明。','']
    md=A/'actual_optimization_handoff_v13_20261008.md';assert not md.exists();md.write_text('\n'.join(lines),encoding='utf8',newline='\n')
    for p,digest in state['input_sha256'].items():assert sha(p)==digest,p
    print('Handoff13 records seven live complete queues and actual1411029-graph controls.',flush=True)

if __name__=='__main__':main()
