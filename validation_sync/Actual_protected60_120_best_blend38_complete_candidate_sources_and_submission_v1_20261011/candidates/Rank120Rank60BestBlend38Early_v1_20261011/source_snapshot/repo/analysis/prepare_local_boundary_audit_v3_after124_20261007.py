"""Refresh verified finite-scope evidence without claiming global exhaustion."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    old=A/'audit_local_optimization_boundaries_v2_20261007.py';new=A/'audit_local_optimization_boundaries_v3_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8').replace('local_optimization_boundary_audit_v2_20261007','local_optimization_boundary_audit_v3_20261007')
    needle='    import psutil\n';assert text.count(needle)==1
    text=text.replace(needle,needle+"    gate=A/'service_owned_workflows_20261006/nonflag_reverse_Ridge40_round124_full_registration_v1'\n    while owned(read(gate/'native_launch.json')):time.sleep(10)\n    assert read(gate/'service_execution.json')['status']=='passed'\n")
    needle="121:'nonflag_Ridge40_round121_full_registration_v1'}";assert text.count(needle)==1
    text=text.replace(needle,"121:'nonflag_Ridge40_round121_full_registration_v1',122:'nonflag_RFFRidge40_round122_full_registration_v1',123:'nonflag_reverse_RFF40_round123_full_registration_v1',124:'nonflag_reverse_Ridge40_round124_full_registration_v1',125:'nonflag_RFF12876_round125_full_registration_v1'}")
    text=text.replace('set(range(107,119))','set(range(107,125))')
    needle="('nonflag_Ridge',121,'nonflag_residual_Ridge_bank10_20261007','nonflag_Ridge40_official_comparison_v1_20261007',10,40)]";assert text.count(needle)==1
    text=text.replace(needle,"""('nonflag_Ridge',121,'nonflag_residual_Ridge_bank10_20261007','nonflag_Ridge40_official_comparison_v1_20261007',10,40),
        ('nonflag_RFF32_positive',122,'nonflag_residual_RFFRidge_bank10_20261007','nonflag_RFFRidge40_official_comparison_v1_20261007',10,40),
        ('nonflag_RFF32_reverse',123,'nonflag_residual_RFFRidge_bank10_20261007','nonflag_reverse_RFF40_official_comparison_v1_20261007',10,40),
        ('nonflag_Ridge_reverse',124,'nonflag_residual_Ridge_bank10_20261007','nonflag_reverse_Ridge40_official_comparison_v1_20261007',10,40),
        ('nonflag_RFF128_both_signs',125,'nonflag_residual_RFF128_bank10_20261007','nonflag_RFF12876_official_comparison_v1_20261007',10,76)]""")
    text=text.replace("item={'family':family,'round':number,", "item={'family':family,'round':number,'source_native_bank':bank_name,'reused_existing_bank_not_new_fits_by_this_audit':True,")
    text=text.replace("'nonflag_Ridge40_continue_after_actual_admission'):","'nonflag_Ridge40_continue_after_actual_admission','nonflag_RFF12876_round125_source_admission_v1','nonflag_RFF12876_continue_after_actual_admission_v2','nonflag_residual_RFF128_native_bank10'):")
    text=text.replace('8个近期模型族的实际年度拟合与官方比较','12个近期模型及后处理路线的实际年度拟合与官方比较；重复银行是复用，不新增或重复累计拟合')
    text=text.replace('119—121完整候选与新比较仍须按实际状态推进','125轮完整候选与新比较仍须按实际状态推进')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [Path(__file__),old,new]}
    create(A/'local_boundary_audit_v3_source_preparation_20261007.json',
      {'status':'compiled_extended_closed_scope_and_actual_native128_boundary_audit','input_sha256':pins,'global_exhaustion_not_claimed':True})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('local_boundary_audit_v3_after124',new.name,[],pins)
    create(A/'local_boundary_audit_v3_hidden_launch_20261007.json',row)
    print({'status':'queued_actual_audit_after_full124','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
