"""Record six complete queues plus the new actual20-model CG bank and frozen141 preliminary plan."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    previous=A/'actual_optimization_handoff_v11_20261008.json';state=read(previous)
    progress=read(A/'actual_optimization135_to140_progress_v9_20261008.json')
    bank_pointer=A/'actual_nonflag_KrylovGram64_bank20_location_v3_20261008.json';bank=Path(read(bank_pointer)['output'])
    causal_pointer=A/'actual_KrylovGram20_causal_refit_location_v2_20261008.json';causal=Path(read(causal_pointer)['output'])
    bp=read(bank/'verification.json');cp=read(causal/'verification.json')
    assert bp['actual_native_fits']==20 and bp['actual_full_OOF_heads']==4
    assert cp['actual_causal_same_configuration_refit_controls']==20 and cp['actual_maturity_windows']==5
    plan=A/'KrylovGram52_round141_plan_v1_20261008.json';assert read(plan)['expected_scored_cases']==52 and read(plan)['anchors']==[138,139,140]
    native=A/'KrylovGram141_native_receiver_preflight_v1_20261008.json';np=read(native)
    assert len(np['adapter_controls'])==7 and np['backend_priority_cases']==7
    launches=A/'actual_KrylovGram52_plan_historical_hidden_launches_v1_20261008.json'
    files=[Path(__file__),previous,bank_pointer,bank/'verification.json',causal_pointer,causal/'verification.json',plan,native,launches,
        A/'prepare_KrylovGram52_round141_plan_controls_v1_20261008.py',A/'prepare_KrylovGram141_native_preflight_v1_20261008.py',
        A/'KrylovGram141_native_preflight_lineage_v1_20261008.json',A/'actual_KrylovGram141_calendar_hidden_launch_v1_20261008.json',
        A/'nonflag_KrylovGram64_controls_main_v2_20261008/probe/receipt.json',A/'nonflag_KrylovGram64_controls_main_v2_20261008/bank/receipt.json']
    for name,item in state['actual_owned_live_services'].items():assert owned(item['identity']),name
    preliminary={}
    for name,row in read(launches)['launches'].items():
        folder=A/'service_owned_workflows_20261006'/name;preliminary[name]={'identity':row,'live':owned(row)}
        if not preliminary[name]['live']:preliminary[name]['terminal']=read(folder/'service_execution.json')
        files += [folder/'native_launch.json',folder/'job_definition.json']
    state.update(status='active_six_complete135140_queues_and_frozen141_preliminary_CG_plan_with_passed20_causal_refits',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),actual_progress_at_checkpoint=progress,
        input_sha256={**state['input_sha256'],**{str(p):sha(p) for p in files}},
        actual_KrylovGram_controls={'native_numerical_recipe':2,'bank_administrative_version':3,'saved_annual_models':20,'full_OOF_heads':4,
            'small_native_fits':12,'small_saved_prefixes':72,'actual200003_probe_fits':4,'probe_saved_prefixes':24,
            'own_maturity_windows':5,'later_TRAIN_label_poison_same_recipe_refits':20,'actual_adapter_contracts':7,
            'small_and_probe_and_bank_main_receipts':[read(A/f'nonflag_KrylovGram64_controls_main_v2_20261008/{phase}/receipt.json') for phase in ('probe','bank')]},
        actual141_preliminary_services=preliminary,actual141_quality={'completed_records':0,'expected_records':52},
        actual141_complete_quality_pipeline_not_yet_prepared=True,
        still_required141=['Finish and publish49 complete5635800 CDF/147cold and24native24cold historical hooks and24calendar48day controls.',
            'Prepare and independently check full141 source routes, all seven parent backends, modelSHA union, D scoring scopes and complete candidate/QA52/main workflows.',
            'After complete140 QA51/main, admit the exact qualified138139140 parent and52 original official comparisons.',
            'Freeze selected whole graph/source/parameters/calibration before actual future X; full native/reload/independent and cold80, or honest exact anchor reuse.',
            'Six full leaderboard views,45second QA52, all prior evidence preserved and verified GitHub main update.'])
    create(A/'actual_optimization_handoff_v12_20261008.json',state)
    best=progress['best_fully_qualified'];epoch=progress['latest_actual_epoch']
    lines=['# 实际优化交接 v12','',f"记录时间：{state['at_local']}；截止：2026年10月10日23:59（UTC+8）。",'',
        f"完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；神经年度完成{len(progress['annual_models_complete'])}/6，{epoch['year']}年度已保存{epoch['saved_epoch']}/{epoch['total_epochs']}轮。",'',
        '135–140六轮完整队列继续运行或等待已验证依赖。第140轮修复与完整队列已同步main。',
        '新增重正交共轭梯度岭回归：12小样本/72保存前缀、4实际20万样本/24前缀、20成熟年度模型/4完整OOF、5窗口/20标签扰动重训练和7完整父接入检查已通过。小样本、实际探测、全部年度模型及失败旧版均已同步main。',
        '第141轮已冻结52项计划（138/139/140三个合格锚点、48项正负CG变换、零幅度恒等对照）；49完整/147冷及24历史原生/24冷检查已启动，跨年检查已启动。',
        '141全评分/冻结/真实候选/QA52/main流程尚待准备，不宣称已运行完整141队列。135–141尚无新增官方质量分。',
        '原GPU训练保持；完整实时进度在actual_optimization135_to140_progress_v9_20261008.md。新模型与缓存均在E。',
        '目标active；没有全局方向或资源穷尽证明。','']
    md=A/'actual_optimization_handoff_v12_20261008.md';assert not md.exists();md.write_text('\n'.join(lines),encoding='utf8',newline='\n')
    for p,digest in state['input_sha256'].items():assert sha(p)==digest,p
    print('Handoff12 preserves six complete queues and records new20-model CG causal controls and preliminary141.',flush=True)

if __name__=='__main__':main()
