"""Queue publication of every actual stronger-parent screen result, never preclaim completion."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    s=(A/'publish_priority_Huber163_temporal73_v10_20261010.py').read_text(encoding='utf8')
    start=s.index('    sources=[');end=s.index("    if phase in ('scores'",start)
    names=['prepare_TopWeighted65_completion_main_v12_20261010.py','run_TopWeighted_after163_high_impact65_screen_v1_20261010.py','TopWeighted_after163_high_impact65_frozen_intent_v1_20261010.json','prepare_new_return_priority_controller_v19_20261010.py','run_continuous_fast_reused_frontiers_v19_20261010.py','handoff_new_return_priority_controller_v19_20261010.py','new_return_priority_handoff_v19_20261010/verification.json','new_return_priority_handoff_v19_20261010/frozen_before_handoff.json','ReturnHuber050_actual_CPU20_fixture_main_receipt_v1_20261010.json']
    s=s[:start]+"    sources=[Path(__file__)]+[A/name for name in "+repr(names)+"]\n"+s[end:]
    for old,new in [('Huber010_high_impact65_screen_v1_20261010','TopWeighted_after163_high_impact65_screen_v1_20261010'),('actual_Huber010_high_impact65_screen_v1_20261010','actual_TopWeighted_after163_high_impact65_screen_v1_20261010'),('actual_Huber010_high_impact65_screen_location_v1_20261010.json','actual_TopWeighted_after163_high_impact65_screen_location_v1_20261010.json'),('main_v10_20261010','main_v12_20261010'),("'+phase+'_v10_20261010","'+phase+'_v12_20261010"),('main_receipt_v10_20261010','main_receipt_v12_20261010')]:s=s.replace(old,new)
    s=s.replace('优先验证实测更高分Huber163并扩展73项因果神经信号平滑','发布新Top加权网络在当前最佳完整163方案之后65项实际组合控制和官方评分')
    target=A/'publish_TopWeighted_after163_65_completion_v12_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    row=start_service('actual_TopWeighted_after163_65_completion_main_v12_20261010',target.name,['huber65'],{str(target):sha(target),str(Path(__file__)):sha(Path(__file__))})
    create(A/'TopWeighted_after163_65_completion_main_hidden_launch_v12_20261010.json',row);print(row,flush=True)
if __name__=='__main__':main()
