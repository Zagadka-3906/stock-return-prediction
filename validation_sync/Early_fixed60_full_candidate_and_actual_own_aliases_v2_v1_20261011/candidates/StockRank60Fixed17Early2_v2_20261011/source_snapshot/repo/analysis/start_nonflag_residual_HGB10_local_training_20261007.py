"""Freeze and launch three hidden local admission/training jobs with E-drive scratch."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    out=A/'nonflag_residual_HGB10_actual_hidden_launches_20261007.json';assert not out.exists()
    jobs=[('nonflag_residual_HGB_codec2_preflight','verify_nonflag_residual_HGB_codec2_20261007.py'),
      ('nonflag_residual_HGB10_training_admission','admit_nonflag_residual_HGB10_training_20261007.py'),
      ('nonflag_residual_HGB10_training','run_nonflag_residual_HGB10_after_admission_20261007.py')]
    paths=[Path(__file__),*[A/s for _,s in jobs],A/'train_nonflag_residual_HGB_bank10_20261007.py',A/'nonflag_residual_HGB10_plan_20261007.json',
      A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'cpu_numerical_HGB_large_batch_codec_v2_20261007.py',A/'memory_bounded_numeric_preparation_20261007.py']
    for p in paths:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    prep=A/'nonflag_residual_HGB10_complete_training_source_preparation_20261007.json';assert not prep.exists()
    create(prep,{'status':'compiled_unlaunched10_nonflag_residual_fit_recipe_and_true_codec_admission','input_sha256':{str(p):sha(p) for p in paths},
      'new_native_fits':0,'new_quality_scores':0,'model_data_or_scratch_on_C':False})
    paths.append(prep);pins={str(p):sha(p) for p in paths};launches={}
    for name,script in jobs:
        try:r=start_service(name,script,[],pins)
        except AssertionError:
            f=A/'service_owned_workflows_20261006'/name;r=read(f/'native_launch.json');assert not owned(r) and read(f/'service_execution.json')['status']=='passed'
        assert r['actual_native_console_handle']==0 and not r['independent_launch_root_in_any_job'];launches[name]=r
    create(out,{'status':'actual_three_hidden_local_nonflag_training_jobs_started','input_sha256':pins,'launches':launches,
      'prospective_selection_fits':10,'prospective_diagnostic_fits':2,'remote_tasks_dispatched':0,'scientific_workers_stopped':0,
      'actual10_fits_scores_future_or_round120_qualification_not_claimed':True,'test_labels_read':False})
    print({'status':'started','actual_jobs':3},flush=True)
if __name__=='__main__':main()
