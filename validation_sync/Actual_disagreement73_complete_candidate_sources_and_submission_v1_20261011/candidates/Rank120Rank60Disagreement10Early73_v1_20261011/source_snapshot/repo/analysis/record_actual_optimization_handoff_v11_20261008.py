"""Record six actual pipelines with complete140 preflight and preserved administrative recovery evidence."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    previous=A/'actual_optimization_handoff_v10_20261008.json';state=read(previous)
    progress=read(A/'actual_optimization135_to140_progress_v9_20261008.json')
    assert progress['observer_version']==9
    proof_path=A/'SpectralGram52_prospective_routes_v2_20261008.json';proof=read(proof_path)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==882 and proof['actual_physical_model_count_controls']==8
    assert len(proof['baseline_controls'])==9 and len(proof['same_score_sort_controls'])==6
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    launches_path=A/'SpectralGram140_complete_hidden_launches_v4_20261008.json'
    files=[Path(__file__),previous,proof_path,launches_path,
        A/'SpectralGram140_complete_dependency_plan_v3_20261008.json',A/'SpectralGram140_receiver_preparation_v2_20261008.json',
        A/'SpectralGram140_truthful_metadata_receiver_preparation_v2_20261008.json',A/'SpectralGram140_exact_idle_metadata_supersession_v1_20261008.json',
        A/'SpectralGram140_registration_admin_path_recovery_v4_20261008.json',A/'SpectralGram140_archive_and_observer_preparation_v2_20261008.json',
        A/'actual_SpectralGram140_completed_CSV_archivist_hidden_launch_v1_20261008.json',A/'actual_optimization135_to140_progress_hidden_launch_v9_20261008.json',
        A/'monitor_actual_optimization135_to140_v9_20261008.py',A/'archive_SpectralGram140_completed_scoring_CSV_v1_20261008.py',
        A/'SpectralGram140_historical_causal_main_v1_20261008/receipt.json']
    services=state['actual_owned_live_services']
    for name,row in read(launches_path)['launches'].items():
        assert owned(row) and row['actual_native_console_handle']==0,name
        services[name]={'round':140,'identity':row,'live':True};folder=A/'service_owned_workflows_20261006'/name
        files += [folder/'native_launch.json',folder/'job_definition.json']
    for name,item in services.items():assert owned(item['identity']),name
    state.update(status='active_six_complete135_to140_queues_with_completed_SpectralGram20_and_causal_and_native_controls',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),actual_progress_at_checkpoint=progress,actual_owned_live_services=services,
        input_sha256={**state['input_sha256'],**{str(p):sha(p) for p in files}},
        actual140_controls=progress['actual140_completed_preliminary_controls'],actual140_quality=progress['actual140_quality'],
        still_required140=['Complete139 QA50 and main; exact qualified137138139 best parent and49full147cold current-parent controls.',
            'All52 original official full8 metrics; publish completed control and score evidence to main.',
            'Freeze selected whole graph, calibration, model/config/source bytes before new future X.',
            'Two full1599600 native/independent replays and cold80, or honest exact qualified anchor reuse with zero new inference.',
            'Unique physical modelSHA union, all six complete leaderboard views,45second QA51 and verified remote main receipt.'],
        actual140_launch_metadata={'round':140,'expected_official_cases':52,'QA_version':51,'science_receiver_version':2,
            'full_registration_receiver_version':3,'administrative_dispatch_version':4,'source_and_failed_launch_evidence_preserved':True},
        remaining_uncovered_directions=['Use completed135140 official results and deadline/resources to assess further bounded combinations and native fits.',
            'The finite declared grids do not prove a global feasible-direction or resource boundary.'])
    target=A/'actual_optimization_handoff_v11_20261008.json';create(target,state)
    best=progress['best_fully_qualified'];epoch=progress['latest_actual_epoch']
    lines=['# 实际优化交接 v11','',f"记录时间：{state['at_local']}；截止：2026年10月10日23:59（UTC+8）。",'',
        f"完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；完整榜{progress['latest_fully_qualified']['connected_records']:,}条。",'',
        f"神经年度完成{len(progress['annual_models_complete'])}/6；{epoch['year']}年度已保存{epoch['saved_epoch']}/{epoch['total_epochs']}轮。",'',
        '135–140六轮完整队列均已运行或等待已验证依赖，保持原GPU训练。第140轮科学接收器2、行政注册接收器3；旧记录字段、重复独占目录和观察器Markdown接口的失败证据均保留。',
        '主成分截断岭回归已实际完成20年度模型/4完整OOF；49完整/147冷CDF；24历史原生/24冷接入；24跨年/48按日；6适配器；5成熟窗口/20次后续训练标签扰动重训练。历史与因果记录已上传main。',
        '24接收器/882完整父图/9基准/6同分排序/8物理SHA计数和原评分目录范围已检查。八步骤队列等待完整139，然后执行52评分、冻结、真实候选、QA51、完整榜main。',
        '135–140尚无新增官方质量分；不把前置正确性检查计作质量提升。',
        '实时进度：actual_optimization135_to140_progress_v9_20261008.md。大文件保存在E，原官方评分目录保留D。',
        '目标保持active。尚无全部可行方向与计算资源边界证明。','']
    md=A/'actual_optimization_handoff_v11_20261008.md';assert not md.exists();md.write_text('\n'.join(lines),encoding='utf8',newline='\n')
    for p,digest in state['input_sha256'].items():assert sha(p)==digest,p
    print('Handoff11 records six live complete queues and true140 counts without unexecuted quality claims.',flush=True)

if __name__=='__main__':main()
