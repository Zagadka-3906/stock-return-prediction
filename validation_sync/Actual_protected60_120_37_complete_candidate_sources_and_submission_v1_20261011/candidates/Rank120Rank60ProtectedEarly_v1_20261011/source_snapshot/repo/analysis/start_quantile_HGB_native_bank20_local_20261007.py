"""Start actual hidden codec4, source admission, and native20 local jobs."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    out=A/'quantile_HGB_native_bank20_actual_hidden_launches_20261007.json';assert not out.exists()
    jobs=[('quantile_HGB_codec4_preflight','verify_quantile_HGB_codec_preflight_20261007.py'),
      ('quantile_HGB_native_bank20_source_admission','admit_quantile_HGB_native_bank20_20261007.py'),
      ('quantile_HGB_native_bank20_training','run_quantile_HGB_native_bank20_after_admission_20261007.py')]
    sources=[Path(__file__),*[A/script for _,script in jobs],A/'train_quantile_HGB_native_bank20_20261007.py',
      A/'quantile_HGB_native_bank20_plan_20261007.json',A/'quantile_HGB_native_bank20_source_preparation_20261007.json',
      A/'cpu_conditional_residual_hgb_codec_20261007.py',A/'direct_flag_centered_rank_CDF_transform_20261007.py',
      ROOT/'后续选模标准.md',ROOT/'evaluate.py']
    pins={str(p):sha(p) for p in sources}
    for p in sources:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    launches={}
    for name,script in jobs:
        try:r=start_service(name,script,[],pins)
        except AssertionError:
            f=A/'service_owned_workflows_20261006'/name;r=read(f/'native_launch.json')
            assert not owned(r) and read(f/'service_execution.json')['status']=='passed',name
        assert r['actual_native_console_handle']==0 and not r['independent_launch_root_in_any_job'];launches[name]=r
    create(out,{'status':'actual_three_local_quantile_HGB_dependency_jobs_started','input_sha256':pins,'launches':launches,
      'remote_tasks_dispatched':0,'native_selection_fits_expected':20,'diagnostic_fits_expected':4,
      'scientific_workers_stopped':0,'actual20_fits_future_inference_or119_qualification_not_claimed':True,'test_labels_read':False})
    print({'status':'started','jobs':3},flush=True)

if __name__=='__main__':main()
