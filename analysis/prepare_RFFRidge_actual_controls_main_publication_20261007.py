"""Schedule append-only publication of the actual new family after prior main writers."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    old=A/'publish_nonflag_residual_Ridge_bank_after120_20261007.py'
    new=A/'publish_nonflag_residual_RFFRidge_bank_after121_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8').replace('nonflag_residual_Ridge','nonflag_residual_RFFRidge').replace('nonflag_Ridge','nonflag_RFFRidge')
    text=text.replace("bank_service=closed('nonflag_residual_RFFRidge_native_bank10')","bank_service=closed('nonflag_residual_RFFRidge_native_bank10_v2')\n    closed('nonflag_RFFRidge_actual_hook3_and_full37_controls')")
    text=text.replace("    from run_nonflag_residual_RFFRidge_hook3_after_bank_20261007 import main as hooks\n    hooks()\n",'')
    text=text.replace("    closed('nonflag_HGB40_round120_full_registration_v4')","    closed('nonflag_Ridge40_round121_full_registration_v1')\n    closed('lossless_string_codec_benchmark_main_after_audit')")
    text=text.replace('waiting_round120_main','waiting_round121_main')
    text=text.replace('independent_linear_state','independent_random_fourier_linear_state')
    text=text.replace('Ridge10年度模型','RFFRidge10年度模型').replace('非涨停残差Ridge：两组训练样本数归一化L2','非涨停残差RFFRidge：两组固定32维随机傅里叶核映射与样本数归一化L2')
    text=text.replace('独立线性状态','独立傅里叶频率与线性状态')
    needle="    sources=[p for p in dict.fromkeys(sources) if p.resolve()!=stage.resolve()]; assert all(p.exists() for p in sources)"
    assert text.count(needle)==1
    text=text.replace(needle,"""    control_proof=A/'nonflag_RFFRidge_actual_native_and_transform_controls_20261007.json'
    assert read(control_proof)['status']=='passed_actual3_native_hooks37_full_CDF_and111_cold_controls'
    sources += [control_proof,A/'prepare_nonflag_RFFRidge_actual_controls_20261007.py',
        A/'run_nonflag_RFFRidge_actual_controls_20261007.py',A/'nonflag_RFFRidge_actual_controls_source_preparation_20261007.json',
        A/'nonflag_RFFRidge40_plan_20261007.json',A/'RFFRidge_zero_fit_admission_label_correction_20261007.json',
        A/'correct_RFFRidge_training_admission_label_before_any_fit_20261007.py',
        A/'prepare_RFFRidge_actual_controls_main_publication_20261007.py',
        *(A/'nonflag_residual_RFFRidge37_transform_preflight_20261007').glob('*.json')]
    zero_fit_failure=A/'service_owned_workflows_20261006/nonflag_residual_RFFRidge_native_bank10'
    assert read(zero_fit_failure/'service_execution.json')['status']=='failed'
    assert not owned(read(zero_fit_failure/'native_launch.json'))
    failed.append({'name':zero_fit_failure.name,'actual_failure':read(zero_fit_failure/'service_execution.json')['failure'],'actual_selection_fits':0})
    sources += [*zero_fit_failure.glob('*.json'),*zero_fit_failure.glob('*.log')]
"""+needle)
    text=text.replace("'actual_official_scores':0,'training_and_native_controls_seconds'", "'actual_full_CDF_controls':37,'actual_cold_prefix_controls':111,\n                'actual_official_scores':0,'training_and_native_controls_seconds'")
    text=text.replace('3个历史603行组件/CDF诊断。未执行官方Ridge选模评分或完整未来候选资格。',
        '3个历史603行组件/CDF诊断，以及37个完整训练期输出和111个日期截断的独立核对。未执行官方RFFRidge选模评分或完整未来候选资格。')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [Path(__file__),old,new]}
    create(A/'RFFRidge_actual_controls_publication_source_preparation_20261007.json',{'status':'compiled_publication_after_actual_native_and_full_controls_and_prior_main_writers','input_sha256':pins})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_RFFRidge_actual_controls_main_after121',new.name,[],pins)
    create(A/'RFFRidge_actual_controls_publication_hidden_launch_20261007.json',row)
    print({'status':'publication_queued','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
