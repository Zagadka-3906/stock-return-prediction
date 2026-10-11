"""Preserve actual zero-fit admission-label failure and launch the corrected trainer."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    folder=A/'service_owned_workflows_20261006/nonflag_residual_RFFRidge_native_bank10'
    assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='failed'
    assert not (A/'nonflag_residual_RFFRidge_bank10_20261007').exists()
    old=A/'train_nonflag_residual_RFFRidge_bank10_20261007.py'
    new=A/'train_nonflag_residual_RFFRidge_bank10_v2_20261007.py';assert not new.exists()
    source=old.read_text(encoding='utf8')
    assert source.count('passed_actual2_Ridge_codec_controls_and10_past_only_fit_admission')==1
    source=source.replace('passed_actual2_Ridge_codec_controls_and10_past_only_fit_admission','passed_actual2_RFFRidge_codec_controls_and10_past_only_fit_admission')
    source=source.replace('nonflag_residual_RFFRidge10_source_admission_20261007.json','nonflag_residual_RFFRidge10_source_admission_v2_20261007.json')
    compile(source,str(new),'exec');new.write_text(source,encoding='utf8',newline='\n')
    original=read(A/'nonflag_residual_RFFRidge10_source_admission_20261007.json')
    assert original['status']=='passed_actual2_RFFRidge_codec_controls_and10_past_only_fit_admission'
    for p,d in original['input_sha256'].items():assert sha(p)==d,p
    proof=A/'RFFRidge_zero_fit_admission_label_correction_20261007.json'
    pins={**original['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),new,folder/'service_execution.json',folder/'stderr.log']}}
    create(proof,{'status':'corrected_only_admission_status_literal_and_new_admission_path_before_any_training',
        'old_source_sha256':sha(old),'new_source_sha256':sha(new),'actual_failed_fit_count':0,
        'parameters_features_mature_windows_and_codec_unchanged':True,'old_actual_failure_retained':True})
    pins[str(proof)]=sha(proof)
    admission=A/'nonflag_residual_RFFRidge10_source_admission_v2_20261007.json'
    create(admission,{**original,'input_sha256':pins,'prior_actual_failure_before_any_fit':str(folder/'service_execution.json')})
    row=start_service('nonflag_residual_RFFRidge_native_bank10_v2',new.name,[],{**pins,str(admission):sha(admission)})
    create(A/'nonflag_residual_RFFRidge10_actual_hidden_launch_v2_20261007.json',row)
    print({'status':'started_corrected_actual_trainer','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
