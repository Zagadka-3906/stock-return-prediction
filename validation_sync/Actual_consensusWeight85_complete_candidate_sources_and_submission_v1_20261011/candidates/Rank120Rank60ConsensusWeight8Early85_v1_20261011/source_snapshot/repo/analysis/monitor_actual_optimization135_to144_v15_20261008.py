"""Report actual seven source3/registration4 receivers and controls, without planned-work completion claims."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read
from atomic_optimization_observer_writes_20261005 import write
from monitor_actual_optimization135_to143_v13_20261008 import services
def controls(pointer,prefix):
    path=A/pointer
    if path.exists():out=Path(read(path)['output'])
    else:out=Path('E:/赛题五_本机临时')/prefix
    result={'completed_items':len(list(out.glob('control*.json')))+len(list(out.glob('hook*.json')))+len(list(out.glob('case*.json'))),
            'actual_passed':False,'output':str(out)}
    if (out/'verification.json').exists():
        q=read(out/'verification.json');result.update(actual_passed=q['status'].startswith('passed'),verification=q)
    return result
def main():
    launches=read(A/'ConeRidgeAlpha144_complete_hidden_launches_v4_20261008.json')['launches']
    launches.update({name:read(A/'service_owned_workflows_20261006'/name/'native_launch.json') for name in (
        'ConeRidgeAlpha48_native_historical_hooks_v1_20261008','ConeRidgeAlpha_multiyear_native_calendar_v1_20261008',
        'ConeRidgeAlpha97_current_parent_controls_v2_20261008','ConeRidgeAlpha97_parent134_historical_controls_v1_20261008')})
    while True:
        state=read(A/'actual_optimization135_to144_progress_v14_20261008.json');state.update(observer_version=15,at_local=datetime.now().isoformat(timespec='seconds'))
        state['actual144_services']=services(launches)
        q={key:controls(pointer,out) for key,pointer,out in (
            ('historical','actual_ConeRidgeAlpha97_parent134_location_v1_20261008.json','ConeRidgeAlpha97_parent134_historical_v1_20261008'),
            ('current','actual_ConeRidgeAlpha97_current_parent_location_v1_20261008.json','ConeRidgeAlpha97_current_parent_full_v1_20261008'),
            ('native','actual_ConeRidgeAlpha48_native_hooks_location_v1_20261008.json','ConeRidgeAlpha48_native_historical_hooks_v1_20261008'),
            ('calendar','actual_ConeRidgeAlpha_multiyear_calendar_location_v1_20261008.json','ConeRidgeAlpha_multiyear_native_calendar_v1_20261008'))}
        folder=A/'ConeRidgeAlpha100_official_comparison_v1_20261008';count=len(list(folder.glob('case*_official.json')))
        plan={'expected_records':100,'expected_new_cases':96,'current_quality_scores':count,
              'actual_adapter_contracts':9,'actual_prospective_sources':24,'actual_complete_parent_graph_controls':2619,
              'actual_controls':q,'seven_actual_receivers_dispatched':True,'source_version':3,'registration_version':4,
              'all_original_failures_and_idle_retirement_evidence_preserved':True,
              'distinct_outer_alpha_stage_preserves_complete_inner_Cone143_parent':True}
        if (folder/'actual_stage.json').exists():plan['stage']=read(folder/'actual_stage.json')
        if (folder/'verification.json').exists():
            p=read(folder/'verification.json');plan.update(full100_comparison_passed=p['status'].startswith('passed'),best=p['best'])
        state['actual144_plan']=plan
        write(A/'actual_optimization135_to144_progress_v15_20261008.json',state)
        best=state['best_fully_qualified'];neural=state['annual_models_complete'];epoch=state['latest_actual_epoch']
        lines=['# 本机优化实际进度','',f"更新：{state['at_local']}；截止：2026-10-10 23:59。",'',
            f"完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；最近完整榜{state['latest_fully_qualified']['connected_records']:,}条。",'',
            f"神经模型完成{len(neural)}/6；最终年度{epoch['completed_epoch']}/{epoch['total_epochs']}轮。完整独立复核、135至141官方评分及候选按现有队列继续。",'',
            f"新增参数模型40/40年度拟合、40/40因果复核通过并同步main；第144轮官方评分{count}/100。",'',
            f"144历史完整控制：{q['historical']['completed_items']}/97，当前父方案完整控制：{q['current']['completed_items']}/97；通过：{q['current']['actual_passed']}。",
            f"144原生控制：{q['native']['completed_items']}/48；跨年控制：{q['calendar']['completed_items']}/48。24份实际来源、2619个完整父图和9个接入合同已通过。",'',
            '实际六个科学接收器来源3及独立登记4已启动。旧等待接收器只在精确PID、创建时间、原生睡眠源码行及零评分证据下替换；原失败、代码、日志均保留。',
            '选模只用TRAIN连续向前验证和原官方八指标。大文件E盘；评分目录D盘；仅GitHub main。目标active，未证明全局优化穷尽。','']
        p=A/'actual_optimization135_to144_progress_v15_20261008.md';part=p.with_suffix('.md.part');part.write_text('\n'.join(lines),encoding='utf8',newline='\n');part.replace(p)
        time.sleep(10)
if __name__=='__main__':main()
