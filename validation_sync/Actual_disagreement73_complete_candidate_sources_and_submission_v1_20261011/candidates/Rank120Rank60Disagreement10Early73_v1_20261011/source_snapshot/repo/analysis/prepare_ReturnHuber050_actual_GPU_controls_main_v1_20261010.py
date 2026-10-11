"""Publish actual return-model restart/CPU inference only after both services pass."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    s=(A/'publish_BF16TopWeightedHuber010165_pretraining_controls_v1_20261010.py').read_text(encoding='utf8')
    s=s.replace('topweightedhuber010','returnhuber050').replace('TopWeightedHuber010165','ReturnHuber050166')
    s=s.replace('import sys, os, gzip, hashlib','import sys, os, gzip, hashlib, time').replace('import read,sha,create','import read,sha,create,owned')
    start=s.index('    restart=Path(')
    wait='''    for name in ('actual_BF16_medium2048_returnhuber050_seed09_restart_control_v1_20261009','BF16ReturnHuber050166_independent_small_CPU_v1_20261009'):
        folder=A/'service_owned_workflows_20261006'/name
        while not (folder/'service_execution.json').exists() or owned(read(folder/'native_launch.json')):
            for control_name in ('current_user_runtime_control_20261009.json','current_user_runtime_control_20261010.json'):
                c=read(A/control_name);assert c['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(c['stop_at_local'])
            time.sleep(15)
        assert read(folder/'service_execution.json')['status']=='passed'
'''
    s=s[:start]+wait+s[start:]
    start=s.index('    paths.extend(A/name for name in (');end=s.index('\n    paths.extend(restart',start)
    s=s[:start]+"    paths.extend(A/name for name in ('ReturnHuber050_independent_targets_loss_gradient_controls_v1_20261010.json','ReturnHuber050_own_bank_controls_source_admission_v1_20261010.json','actual_ReturnHuber050_past_fixture_location_v1_20261010.json','actual_optimization_fast_runtime_handoff_v15_20261010.json','ReturnHuber050_actual_CPU20_fixture_main_receipt_v1_20261010.json'))"+s[end:]
    s=s.replace("'own_Huber_delta':.1,'own_top_sample_weight':5.,'own_top_training_rank_threshold':.9,'actual_closed_form_loss_gradient_micro_tail_cases':20,'rank_target':True", "'own_Huber_delta':.5,'target':'y_ret_1d','target_scale':20.,'mature_training_only_winsor_quantiles':[.005,.995],'actual_closed_form_loss_gradient_micro_tail_cases':20,'rank_target':False")
    s=s.replace('保存Top加权Huber实际两项断点恢复与10017行独立CPU控制及当前最佳方案之后65项组合计划','发布直接收益率宽网络两项实际GPU断点恢复和10017行独立CPU推理，尚未计分')
    target=A/'publish_ReturnHuber050166_actual_GPU_controls_v1_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    row=start_service('ReturnHuber050166_actual_GPU_controls_main_v1_20261010',target.name,[],{str(target):sha(target),str(Path(__file__)):sha(Path(__file__))})
    create(A/'ReturnHuber050166_actual_GPU_controls_main_hidden_launch_v1_20261010.json',row);print(row,flush=True)
if __name__=='__main__':main()
