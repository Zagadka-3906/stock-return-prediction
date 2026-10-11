"""Prepare publication of actual auxiliary controls, preserved failures, and new solver identities."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    old=A/'publish_epoch_checkpoint_CPU32_actual_controls_20261007.py';new=A/'publish_actual_resume_new_controls_main_20261007.py'
    text=old.read_text(encoding='utf8').replace('epoch_checkpoint_CPU32_actual_controls_github_20261007','actual_resume_new_controls_github_20261007')
    begin=text.index('    proof_path=');end=text.index('    sources=list(dict.fromkeys(sources));',begin)
    sources=[A/'actual_user_resume_until2355_20261007.json',A/'future129_130_131_administrative_count_routes_actual_20261007.json',
      A/'verify_future129_130_131_administrative_count_routes_20261007.py',A/'actual_future_QA40_41_42_E_storage_20261007.json',
      A/'actual_new_streamed_RFF_and_empirical_Bayes_scientific_identity_20261007.json',A/'record_actual_new_science_and_E_QA_storage_20261007.py',
      A/'nonflag_RidgeFine52_administrative52_count_recovery_v2_20261007.json',A/'recover_nonflag_RidgeFine52_full128_counts_v2_20261007.py',
      A/'nonflag_RFF128StreamMid129_dependency_gate_recovery_v2_20261007.json',A/'recover_nonflag_RFF128StreamMid129_dependency_gate_v2_20261007.py',
      A/'nonflag_EmpiricalBayes130_parent128_gate_recovery_v4_20261007.json',A/'recover_nonflag_EmpiricalBayes130_parent128_gate_v4_20261007.py',
      A/'nonflag_EmpiricalBayes130_actual_admission_gate_finalization_v5_20261007.json',A/'finalize_nonflag_EmpiricalBayes130_actual_admission_gate_v5_20261007.py',
      A/'nonflag_EmpiricalBayes40_control_gate_recovery_v2_20261007.json',A/'nonflag_EmpiricalBayes40_full_control_recovery_v3_20261007.json',
      A/'nonflag_EmpiricalBayes40_partial_preparation_failure_20261007.json',A/'nonflag_residual_EmpiricalBayes37_transform_preflight_20261007/verification.json',
      A/'nonflag_residual_EmpiricalBayes64_native_hook3_preflight_20261007/verification.json',
      A/'nonflag_residual_RidgeMicro37_transform_preflight_20261007/verification.json',A/'monitor_full_actual_optimization_until2355_v28_20261007.py']
    sources.extend(p for p in A.glob('*RidgeMicro*20261007.*') if p.suffix in ('.py','.json'))
    for name in ['nonflag_RidgeFine52_round128_full_registration_v1','nonflag_RFF128StreamMid76_actual129_after128_queue',
      'nonflag_residual_EmpiricalBayes37_transform_preflight','nonflag_residual_EmpiricalBayes37_transform_preflight_v2']:
        folder=A/'service_owned_workflows_20261006'/name;assert read(folder/'service_execution.json')['status']=='failed'
        sources.extend([*folder.glob('*.json'),*folder.glob('*.log')])
    source_lines='\n'.join('      A/'+repr(str(p.relative_to(A)).replace('\\','/'))+',' for p in dict.fromkeys(sources))
    replacement="    dependency=A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_full37_controls_main_publication_v1'\n    while not (dependency/'native_launch.json').exists() or owned(read(dependency/'native_launch.json')):\n        assert time.time()<datetime.fromisoformat('2026-10-07T23:35:00+08:00').timestamp()\n        time.sleep(10)\n    assert read(dependency/'service_execution.json')['status']=='passed'\n    proof_path=A/'future129_130_131_administrative_count_routes_actual_20261007.json';proof=read(proof_path)\n    assert proof['status']=='passed_actual72_prospective_sources_all_administrative_record_counts' and not proof['issues']\n    sources=[Path(__file__),A/'prepare_actual_resume_new_controls_main_publication_20261007.py',\n"+source_lines+"\n    ]\n"
    text=text[:begin]+replacement+text[end:]
    text=text.replace("'actual_GPU_training_adapter_not_yet_admitted':True", "'auxiliary_controls_not_new_official_score_records':True")
    text=text.replace('validation_sync/epoch_checkpoint_CPU32_actual_controls_20261007','validation_sync/actual_resume_new_controls_20261007')
    text=text.replace('published_actual_CPU32_fresh_process_epoch_resume_controls','published_actual72_route_controls_37_full111_cold_and_explicit_new_solver_identities')
    text=text.replace("'actual_GPU_equivalence_not_yet_verified':True,", "'actual_administrative_failures_preserved':True,")
    oldnote="训练恢复点实际核对：连续32轮与独立进程7轮保存再继续25轮，CPU权重、训练损失、预处理与预测逐位一致；篡改训练输入被拒绝。保留首轮Windows只读句柄fsync失败及写句柄修复记录。GPU等价性尚待验证，当前16384年度训练仍使用原程序；没有新增正式年度模型或评分。仅main。"
    newnote="实际恢复工作记录：遵照用户继续至23:55的答复；72份后续登记源码的项数控制、微幅Ridge37项全量与111冷前缀核对、分块RFF与自适应标量/对角先验20个成熟年度模型的明确方法身份，以及E盘QA目录核对。保留原始登记项数失败及后续依赖恢复记录；没有以此增加官方分数或宣称完整候选已合格。仅main，未读取真实测试标签。"
    assert oldnote in text;text=text.replace(oldnote,newnote).replace('记录神经训练按轮次落盘与独立进程恢复的实际CPU32核对','记录恢复优化后的实际控制验证、方法身份、E盘输出与失败恢复')
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    create(A/'actual_resume_new_controls_publication_preparation_20261007.json',{'status':'compiled_actual_auxiliary_controls_main_publication_after129_controls_closure',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,*sources]},'new_quality_scores':0})

if __name__=='__main__':main()
