"""Publish actual CPU target/loss checks and mature fixture metadata, without labels."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    src=(A/'publish_BF16TopWeightedHuber010165_pretraining_controls_v1_20261010.py').read_text(encoding='utf8')
    start=src.index('    restart=Path(');end=src.index('    import publish_classifier',start)
    checks='''    proof=read(A/'ReturnHuber050_independent_targets_loss_gradient_controls_v1_20261010.json')
    assert len(proof['records'])==20 and proof['status'].startswith('passed20_CPU')
    admission=read(A/'ReturnHuber050_own_bank_controls_source_admission_v1_20261010.json')
    for p,d in admission['input_sha256'].items():assert sha(p)==d,p
    fixture=Path(read(A/'actual_ReturnHuber050_past_fixture_location_v1_20261010.json')['output'])
    paths=[Path(__file__),A/'prepare_ReturnHuber050_CPU_evidence_publication_v1_20261010.py',A/'ReturnHuber050_independent_targets_loss_gradient_controls_v1_20261010.json',A/'ReturnHuber050_own_bank_controls_source_admission_v1_20261010.json',A/'actual_ReturnHuber050_past_fixture_location_v1_20261010.json',fixture/'verification.json',ROOT/'后续选模标准.md']
    for pattern in ('*returnhuber050*.py','*returnhuber050*.json','*ReturnHuber050*.py','*ReturnHuber050*.json','prepare_medium_return_Huber050*.py','verify_medium_return_Huber050*.py','prepare_returnHuber050*.py'):
        paths.extend(p for p in A.glob(pattern) if p.is_file())
'''
    src=src[:start]+checks+src[end:]
    src=src.replace('BF16TopWeightedHuber010165_pretraining_controls_v1_20261010','ReturnHuber050_actual_CPU20_fixture_controls_v1_20261010').replace('BF16TopWeightedHuber010165_pretraining_main_v1_20261010','ReturnHuber050_actual_CPU20_fixture_main_v1_20261010').replace('BF16TopWeightedHuber010165_pretraining_controls_main_receipt_v1_20261010.json','ReturnHuber050_actual_CPU20_fixture_main_receipt_v1_20261010.json')
    start=src.index("h.sync.encoded({'status':'actual_pretraining");end=src.index('\n    out=',start)
    src=src[:start]+"h.sync.encoded({'status':'actual_CPU20_target_loss_gradient_checks_and_real_mature_fixture_passed','files':bindings,'actual_CPU_controls':20,'target':'y_ret_1d','target_scale':20.,'train_only_winsor_quantiles':[.005,.995],'Huber_delta':.5,'GPU_restart_checks_not_yet_executed':True,'actual_annual_fits':0,'quality_score_records':0,'future_X_read':False,'test_labels_read':False,'raw_fixture_arrays_uploaded':False,'deadline_local':control['stop_at_local']})"+src[end:]
    src=src.replace('保存Top加权Huber实际两项断点恢复与10017行独立CPU控制及当前最佳方案之后65项组合计划','保存直接收益率宽网络20项实际CPU目标损失梯度检查及成熟训练样本证明，GPU验证待执行')
    target=A/'publish_ReturnHuber050_actual_CPU20_fixture_controls_v1_20261010.py'
    assert not target.exists();compile(src,str(target),'exec');target.write_text(src,encoding='utf8',newline='\n')
    row=start_service('ReturnHuber050_actual_CPU20_fixture_main_v1_20261010',target.name,[],{str(target):sha(target),str(Path(__file__)):sha(Path(__file__))})
    create(A/'ReturnHuber050_actual_CPU20_fixture_main_hidden_launch_v1_20261010.json',row);print(row,flush=True)
if __name__=='__main__':main()
