"""Use the idle GPU while160 performs CPU-only registration of an exactly reused candidate."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,runpy,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json')
    assert c['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(c['stop_at_local'])
    for name in ('ReusedNN160Quality19_selected_candidate_sealing_v1_20261009','ReusedNN160Stage_actual_native14_calendar_v1_20261009',
                 'actual_BF16_medium2048_huber010_seed09_restart_control_v1_20261009','BF16Huber010161_independent_small_CPU_v1_20261009'):
        f=A/'service_owned_workflows_20261006'/name
        assert (f/'service_execution.json').is_file() and not owned(read(f/'native_launch.json')) and read(f/'service_execution.json')['status']=='passed',name
    ready_path=A/'ReusedNN160Quality19_selected_release_v1_20261009/selected_candidate_ready_for_registration.json'
    ready=read(ready_path)
    assert ready['new_inference_claimed'] is False and ready['sealed_candidate_complete'] is True
    assert ready['selected_configuration']['model'] is None and ready['selected_configuration']['anchor_round']==159
    quality=A/'ReusedNN160Quality19_official_comparison_v1_20261009/verification.json'
    assert len(read(quality)['records'])==19 and read(quality)['best']==ready['best']
    assert read(A/'optimization_20261003_r159/full_registration_execution.json')['status']=='passed'
    trainer=A/'train_neural_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009.py'
    create(A/'Huber010_actual_idle_GPU_overlap160_v1_20261010.json',{'status':'frozen_verified_GPU_overlap_before_own_Huber_annual_training','at_local':datetime.now().isoformat(),
        'ready_selected_candidate_reuses_exact159_without_future_inference':True,'all160_native14_GPU_controls_closed':True,
        'own_Huber_restart_and_CPU_oracle_closed_passed':True,'original_trainer_and_scientific_math_unchanged':True,
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),trainer,ready_path,quality,A/'optimization_20261003_r159/full_registration_execution.json')},
        'no_forecast_or_score_change_by_overlap':True,'new_quality_scores':0,'test_labels_read':False})
    runpy.run_path(str(trainer),run_name='__main__')
if __name__=='__main__':main()
