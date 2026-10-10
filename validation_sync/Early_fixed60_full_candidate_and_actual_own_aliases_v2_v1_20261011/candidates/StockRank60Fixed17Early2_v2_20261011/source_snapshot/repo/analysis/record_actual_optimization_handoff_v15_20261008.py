"""Snapshot own-calendar receiver3 replacement and actual independent142 scoring progress."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    old=A/'actual_optimization_handoff_v14_20261008.json';state=read(old)
    progress=read(A/'actual_optimization135_to142_progress_v12_20261008.json');assert progress['observer_version']==12
    files=[Path(__file__),old,A/'KrylovGram141_complete_hidden_launches_v3_20261008.json',A/'KrylovGram52_prospective_routes_v3_20261008.json',
        A/'KrylovGram141_calendar_evidence_receiver_recovery_v3_20261008.json',A/'KrylovGram141_exact_idle_metadata_supersession_v1_20261008.json',
        A/'KrylovGram141_corrected_archive_and_observer_hidden_launches_v2_20261008.json',A/'ConeRidge142_historical_causal_main_v1_20261008/receipt.json']
    live={}
    for name,row in read(files[2])['launches'].items():
        assert owned(row) and row['actual_native_console_handle']==0
        live[name]={'identity':row,'live':True};files += [A/'service_owned_workflows_20261006'/name/'native_launch.json',A/'service_owned_workflows_20261006'/name/'job_definition.json']
    state.update(status='active_eight_implemented_queues_with_own141_calendar_binding_and_actual142_scores',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),actual_progress_at_checkpoint=progress,
        actual141_controls=progress['actual141_completed_preliminary_controls'],actual141_owned_services=live,
        actual141_launch_metadata={'round':141,'expected_official_cases':52,'QA_version':52,'science_receivers':3,
            'native_numerical_recipe':2,'bank_administration':3,'eligible_parents':[138,139,140],
            'own_KrylovGram24calendar48day_bound':True,'old_frozen2_sources_preserved':True},
        actual142_controls=progress['actual142_completed_controls'],actual142_quality=progress['actual142_quality'],
        actual141_old_idle_eight_receivers_retired_before_any_quality=True,
        input_sha256={**state['input_sha256'],**{str(p):sha(p) for p in files}})
    create(A/'actual_optimization_handoff_v15_20261008.json',state)
    q=progress['actual142_quality'];epoch=progress['latest_actual_epoch']
    md=A/'actual_optimization_handoff_v15_20261008.md';assert not md.exists()
    md.write_text('\n'.join(['# 实际优化交接 v15','',f"记录：{state['at_local']}；截止2026-10-10 23:59。",'',
        f"神经年度完成5/6，最终年度完成{epoch['completed_epoch']}/32轮；独立CPU142已完成{q['completed_records']}/52官方比较。",'',
        '第142轮历史49完整/147冷、24原生/24冷、24跨年/48按日、20原生扰动重训已通过并同步main；继续评分、完整冻结、候选复核、六视图45秒QA53及完整榜main。',
        '第141轮源版本3修正接入证据绑定：原版本2错误引用Spectral跨年记录，实际CG自身24跨年/48日早已通过。24接收器/1029完整父图重新通过；仅替换精确识别的八个空闲接收器，模型、网格、物理输出及评分数学未改变。',
        '原神经训练及135至140/142工作保持运行。最新进度actual_optimization135_to142_progress_v12_20261008.md。',
        '原始失败及旧冻结来源全部保留。目标active，尚无全局资源或优化穷尽证据。','']),encoding='utf8',newline='\n')
    for p,digest in state['input_sha256'].items():assert sha(p)==digest,p
    print('Handoff15 records corrected141 own calendar and actual142 partial scoring.',flush=True)

if __name__=='__main__':main()
