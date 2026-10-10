"""Publish actual negative controls and remaining feasible frontier; no new official score claim."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    old=A/'publish_epoch_checkpoint_CPU32_actual_controls_20261007.py';new=A/'publish_reverse_Bayes_actual_controls_main_20261007.py'
    text=old.read_text(encoding='utf8').replace('epoch_checkpoint_CPU32_actual_controls_github_20261007','reverse_Bayes_actual_controls_github_20261007')
    begin=text.index('    proof_path=');end=text.index('    sources=list(dict.fromkeys(sources));',begin)
    sources=[A/'prepare_reverse_empirical_Bayes_actual_controls_20261007.py',A/'run_reverse_empirical_Bayes_actual_controls_20261007.py',
      A/'nonflag_ReverseBayes40_control_plan_20261007.json',A/'nonflag_ReverseBayes40_control_source_preparation_20261007.json',
      A/'nonflag_ReverseBayes40_controls_actual_hidden_launch_20261007.json',A/'nonflag_residual_ReverseBayes64_native_stage_20261007.py',
      A/'run_nonflag_residual_ReverseBayes64_hook3_after_bank_20261007.py',A/'verify_nonflag_residual_ReverseBayes37_transform_20261007.py',
      A/'record_remaining_feasible_optimization_frontier_20261007.py',A/'remaining_feasible_optimization_frontier_manual_resume_20261007.json',
      A/'record_actual_single_host_resource_boundary_20261007.py',A/'actual_single_host_resource_boundary_after_resume_20261007.json']
    for folder in [A/'nonflag_residual_ReverseBayes64_native_hook3_preflight_20261007',A/'nonflag_residual_ReverseBayes37_transform_preflight_20261007',A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual_native3_full37_controls']:
        sources.extend([*folder.glob('*.json'),*folder.glob('*.log')])
    replacement="    proof_path=A/'nonflag_ReverseBayes40_actual_native3_full37_cold111_controls_20261007.json';proof=read(proof_path)\n    assert proof['status']=='passed_actual_signed_native3_full37_independent_CDF_and111_cold_controls'\n    assert proof['new_quality_scores']==0 and proof['residual_sign']==-1\n    sources=[Path(__file__),proof_path,A/'prepare_reverse_Bayes_controls_main_publication_20261007.py',\n"+'\n'.join('      A/'+repr(str(p.relative_to(A)).replace('\\','/'))+',' for p in sources)+"\n    ]\n"
    text=text[:begin]+replacement+text[end:]
    text=text.replace("'actual_GPU_training_adapter_not_yet_admitted':True", "'signed_scheme_not_yet_officially_scored_or_adopted':True")
    text=text.replace('validation_sync/epoch_checkpoint_CPU32_actual_controls_20261007','validation_sync/reverse_Bayes_actual_controls_20261007')
    text=text.replace('published_actual_CPU32_fresh_process_epoch_resume_controls','published_actual_reverse_Bayes_native3_full37_cold111_controls')
    text=text.replace("'actual_GPU_equivalence_not_yet_verified':True,", "'official_scores_and_full_candidate_not_yet_claimed':True,'residual_sign':-1,")
    oldnote="训练恢复点实际核对：连续32轮与独立进程7轮保存再继续25轮，CPU权重、训练损失、预处理与预测逐位一致；篡改训练输入被拒绝。保留首轮Windows只读句柄fsync失败及写句柄修复记录。GPU等价性尚待验证，当前16384年度训练仍使用原程序；没有新增正式年度模型或评分。仅main。"
    note="反向自适应收缩实际预检查：复用已验证的标量先验、对角先验及等权均值，明确负残差方向；3项原生重载与独立解码、37项5635800行独立CDF、111项冷前缀全部通过。尚未进行40项官方比较、选中方案冻结、真实完整候选推理或完整榜登记；没有新增模型训练或官方评分。另附本机资源事实及仍可行的交叉模型集成、稀疏线性模型等方向，未宣称优化穷尽。仅main；今晚23:55停工，明早须用户实际发送继续。"
    assert oldnote in text;text=text.replace(oldnote,note).replace('记录神经训练按轮次落盘与独立进程恢复的实际CPU32核对','记录负向自适应收缩实际3/37/111控制与未穷尽方向和资源证据')
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    create(A/'reverse_Bayes_controls_main_publication_preparation_20261007.json',{'status':'compiled_actual_negative_controls_and_frontier_main_publication',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,*sources]},'new_quality_scores':0})

if __name__=='__main__':main()
