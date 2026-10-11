"""Record the concrete immediate CPU142 queue, completed constrained controls and pending work."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    progress=read(A/'actual_optimization135_to142_progress_v11_20261008.json');assert progress['observer_version']==11
    previous=A/'actual_optimization_handoff_v13_20261008.json'
    files=[Path(__file__),previous,A/'ConeRidge142_complete_hidden_launches_v1_20261008.json',
        A/'ConeRidge142_complete_dependency_plan_v1_20261008.json',A/'ConeRidge52_prospective_routes_v1_20261008.json',
        A/'ConeRidge142_archive_and_observer_hidden_launches_v1_20261008.json',A/'ConeRidge64_controls_main_v1_20261008/causal/receipt.json']
    live={}
    for name,row in read(files[2])['launches'].items():
        assert row['actual_native_console_handle']==0
        live[name]={'identity':row,'live':owned(row)}
        files += [A/'service_owned_workflows_20261006'/name/'native_launch.json',A/'service_owned_workflows_20261006'/name/'job_definition.json']
    state={'status':'active_existing_seven_queues_plus_concrete_independent_CPU142',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deadline_local':'2026-10-10T23:59:00+08:00',
        'goal_active_not_paused_complete_or_blocked':True,'actual_progress_at_checkpoint':progress,
        'actual142_controls':progress['actual142_completed_controls'],'actual142_quality':progress['actual142_quality'],
        'actual142_owned_services':live,'actual142_eligible_already_qualified_parents':[132,133,134],
        'actual142_launch_metadata':{'round':142,'expected_official_cases':52,'QA_version':53,'science_receivers':1,'dispatcher':2,
            'native_recipe':1,'independent_BVLS_controls':2,'native_models':20,'own_mature_windows':5,'causal_refits':20,
            'unfinished135141_dependency':False},
        'original135141_frozen_sources_unchanged_by_new142_queue':True,
        'still_required142':['Complete49 full147 cold and24 native24 cold current-parent controls and verified main.',
            'All52 original official8 metric comparisons and score publication on main.',
            'Freeze selected complete model/config/source/graph/calibration before new actual future X.',
            'Two1599600-row native independent replays and cold80 or honest exact qualified anchor reuse with zero new inference.',
            'Full six leaderboard views,45second QA53, unique physical modelSHA counts and verified main.'],
        'independent_oracle_failed_strict_bound_v1_preserved':True,'new_official_scores_by_handoff':0,
        'test_labels_read':False,'global_exhaustion_or_completion_not_claimed':True,
        'input_sha256':{str(p):sha(p) for p in files}}
    create(A/'actual_optimization_handoff_v14_20261008.json',state)
    best=progress['best_fully_qualified'];epoch=progress['latest_actual_epoch']
    lines=['# 实际优化交接 v14','',f"记录：{state['at_local']}；截止：2026-10-10 23:59（UTC+8）。",'',
        f"完整合格最佳第{best['round']}轮，S={best['official_score']:.12f}；神经年度完成{len(progress['annual_models_complete'])}/6，最终年度{epoch['completed_epoch']}/{epoch['total_epochs']}轮。",'',
        '135至141原计划保留。第142轮独立CPU路线已具体实施：已合格132、133、134为锚点，52项官方比较，完整冻结与候选推理、六视图45秒QA53、main均有执行器。',
        '20年度约束岭回归模型、4完整OOF、5成熟窗口/20次标签扰动重训均通过并同步main；12小样本/72前缀及4实际20万行/24前缀通过。',
        '8实际父方案接入、24接收器/1176完整父图、9基准/6同分/8物理SHA和9原D评分范围检查通过。历史49/147及24原生的完成状态以checkpoint证据为准。',
        '失败独立求解器边界断言及三处新接收器构建/检查失败均保留；修复只针对明确数值边界、模板与引用，未修改已冻结模型或评分数学。',
        '进度：actual_optimization135_to142_progress_v11_20261008.md。大文件E，原评分目录D。目标active；尚无全局穷尽证据。','']
    md=A/'actual_optimization_handoff_v14_20261008.md';assert not md.exists();md.write_text('\n'.join(lines),encoding='utf8',newline='\n')
    for p,digest in state['input_sha256'].items():assert sha(p)==digest,p
    print('Handoff14 records concrete independent CPU142 and honest remaining work.',flush=True)

if __name__=='__main__':main()
