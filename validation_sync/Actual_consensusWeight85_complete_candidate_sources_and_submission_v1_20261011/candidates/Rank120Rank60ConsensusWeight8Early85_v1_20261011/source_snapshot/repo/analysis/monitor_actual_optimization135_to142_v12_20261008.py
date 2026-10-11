"""Observe corrected141 receiver3 and actual independent142 scores without changing science."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write

def main():
    launches=read(A/'KrylovGram141_complete_hidden_launches_v3_20261008.json')['launches']
    while True:
        state=read(A/'actual_optimization135_to142_progress_v11_20261008.json')
        state.update(observer_version=12,upstream_at_local=state['at_local'],at_local=datetime.now().isoformat(timespec='seconds'))
        services={}
        for name,row in launches.items():
            item={'live':owned(row),'owned_worker_pid':row['owned_worker_pid'],'actual_native_console_handle':row['actual_native_console_handle'],'driver':row['original_driver']}
            folder=A/'service_owned_workflows_20261006'/name
            if not item['live'] and (folder/'service_execution.json').exists():item['terminal']=read(folder/'service_execution.json')
            services[name]=item
        state['actual141_services']=services;state['actual141_science_receiver_version']=3
        state['actual141_calendar_evidence_is_own_KrylovGram_not_other_family']=True
        state['actual141_calendar_receiver_recovery']=read(A/'KrylovGram141_calendar_evidence_receiver_recovery_v3_20261008.json')
        write(A/'actual_optimization135_to142_progress_v12_20261008.json',state)
        best=state['best_fully_qualified'];epoch=state['latest_actual_epoch'];q=state['actual142_quality']
        lines=['# 本机优化实际进度','',f"更新：{state['at_local']}；截止：{state['deadline_local']}。",'',
            f"完整合格最佳第{best['round']}轮，S={best['official_score']:.12f}；完整榜{state['latest_fully_qualified']['connected_records']:,}条。",'',
            f"神经年度完成{len(state['annual_models_complete'])}/6；最终年度完成{epoch['completed_epoch']}/{epoch['total_epochs']}轮。训练损失不是验证分。" if epoch else '神经年度训练继续。','',
            f"独立CPU第142轮：实际官方比较{q['completed_records']}/52项；完整候选合格状态：{q['fully_qualified']}。",'',
            '第142轮不等待135至141，固定已合格132、133、134比较；20模型/4OOF、20扰动重训、49完整147冷、24原生24冷、24跨年48按日检查实际通过并同步main。',
            '第141轮用新接收器版本3绑定自身CG跨年证据；原版本2全部保留，替换的仅为精确识别且尚未评分的空闲接收器。训练进程未停止或重启。',
            '下一步按已启动执行器完成52分数发布、完整方案冻结、候选原生及独立推理或合格锚点复用、六视图45秒QA53与完整榜main。',
            '大文件E，原评分目录D。目标active，尚无全局可行方向或计算资源边界证据。','']
        target=A/'actual_optimization135_to142_progress_v12_20261008.md';temporary=target.with_suffix('.md.part')
        temporary.write_text('\n'.join(lines),encoding='utf8',newline='\n');temporary.replace(target);time.sleep(10)

if __name__=='__main__':main()
