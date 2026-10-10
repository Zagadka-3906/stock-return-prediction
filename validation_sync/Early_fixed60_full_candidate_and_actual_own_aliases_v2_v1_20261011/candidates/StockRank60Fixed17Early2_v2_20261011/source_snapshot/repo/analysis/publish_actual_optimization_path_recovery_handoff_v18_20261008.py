"""Publish actual score5 recovery, closed proof records and failures after complete135 controls publication."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    prior=A/'service_owned_workflows_20261006/BF16wide40_controls_main_publication_v4_20261008'
    while owned(read(prior/'native_launch.json')):time.sleep(10)
    assert read(prior/'service_execution.json')['status']=='passed'
    source=A/'record_and_publish_actual_optimization_handoff_v17_20261008.py';text=source.read_text(encoding='utf8')
    text=text.replace('actual_optimization135_to144_progress_v15_20261008.json','actual_optimization135_to144_progress_v17_20261008.json')
    text=text.replace('actual_optimization_handoff_v17_','actual_optimization_handoff_v18_').replace('actual_optimization_handoff_main_v17_','actual_optimization_handoff_main_v18_')
    text=text.replace('monitor_actual_optimization135_to144_v15_20261008.py','monitor_actual_optimization135_to144_v17_20261008.py')
    text=text.replace("A/'actual_optimization135_to144_observer_hidden_launch_v15_20261008.json'","A/'actual144_score5_observer_archive_hidden_launches_v17_20261008.json'")
    needle='    sources=list(dict.fromkeys(sources));assert all(p.is_file() and p.suffix in (\'.py\',\'.json\',\'.log\') for p in sources)'
    assert text.count(needle)==1
    text=text.replace(needle,"    sources += [A/'reconcile_actual_handoff17_remote_and_long_paths_v2_20261008.py',A/'actual_handoff17_long_paths_reconciliation_v2_20261008.json',A/'actual_optimization_handoff_main_v17_20261008/receipt.json',A/'start_actual144_score5_observer_and_archive_v17_20261008.py',Path(__file__)]\n"+needle)
    text=text.replace("'actual144_source_version':3,'actual144_registration_version':4", "'actual144_source_version':4,'actual144_scoring_version':5,'actual144_registration_version':6")
    text=text.replace('神经6个年度模型及最终32轮训练已经完成；135至141的完整独立复核、评分、冻结推理与登记继续。',
        '神经6个年度模型、32轮训练、5个完整年度独立复核、37完整/111冷及3原生/3冷均已通过；第135轮实际控制已同步main并开始40项评分。136至141继续队列。')
    text=text.replace('六个科学接收器来源3与独立登记4已启动，尚不能宣称100评分、候选及QA55完成。',
        '原生数学保持不变；评分输出路径与进度写入的旧配置失败保留。新来源4的24脚本/2619完整图、新D评分路径5及E进度写入实际验证后，评分5、候选5和登记6已启动；按实时快照记载实际已完成评分数量，尚不能宣称100评分、候选及QA55完成。')
    text=text.replace('交接17','交接18').replace('handoff17','handoff18')
    target=A/'record_and_publish_actual_optimization_handoff_v18_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'actual_handoff18_source_preparation_20261008.json',{
        'status':'frozen_actual_source4_score5_path_recovery_and_neural135_control_completion_handoff18',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),source,target)},'new_quality_scores':0})
    # Target main() publishes current closed immutable artifacts; helper __file__ remains its true frozen filename.
    namespace={'__file__':str(target),'__name__':'actual_handoff18_publication'}
    exec(compile(text,str(target),'exec'),namespace);namespace['main']()
if __name__=='__main__':main()
