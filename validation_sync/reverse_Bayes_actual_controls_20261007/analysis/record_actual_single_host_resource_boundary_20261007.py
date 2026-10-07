"""Read-only resource evidence; distinguish local bottlenecks from global optimization exhaustion."""
from pathlib import Path
import sys,time,subprocess,shutil,psutil,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    row=read(A/'service_owned_workflows_20261006/neural16384_annual/native_launch.json');assert owned(row)
    result=subprocess.run(['nvidia-smi','--query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu','--format=csv,noheader,nounits'],
      capture_output=True,text=True,encoding='utf8',creationflags=subprocess.CREATE_NO_WINDOW,timeout=20,check=True)
    values=[x.strip() for x in result.stdout.strip().split(',')];assert len(values)==5
    storage=read(A/'neural16384_full_storage_20261005.json');bank=Path(storage['output_directory'])
    infos=sorted(bank.glob('*/info_202[0-5].json'));years=sorted(read(p)['year'] for p in infos)
    native_files=sorted(p for p in bank.rglob('*') if p.is_file() and p.suffix in ('.joblib','.json'))
    sources=[Path(__file__),A/'service_owned_workflows_20261006/neural16384_annual/native_launch.json',A/'neural16384_full_storage_20261005.json',*infos]
    create(A/'actual_single_host_resource_boundary_after_resume_20261007.json',{
      'status':'actual_resource_snapshot_not_global_exhaustion_proof','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'GPU':{'name':values[0],'total_MiB':int(values[1]),'used_MiB':int(values[2]),'free_MiB':int(values[3]),'utilization_percent':int(values[4])},
      'available_RAM_GiB':psutil.virtual_memory().available/2**30,'D_free_GiB':shutil.disk_usage(ROOT).free/2**30,'E_free_GiB':shutil.disk_usage('E:/').free/2**30,
      'actual_owned_large_neural_worker':row,'completed_saved_annual_years':years,'native_info_hashes':{str(p):sha(p) for p in infos},
      'running_original_fitter_saves_only_after_complete_annual_fit':True,'current_unsaved_annual_work_not_durable_across_poweroff':True,
      'no_GPU_checkpoint_equivalence_test_launched_under_current_VRAM_pressure':True,
      'future_GPU_checkpoint_adapter_requires_separate_actual_GPU_validation_before_adoption':True,
      'CPU32_epoch_restart_equivalence_proof':str(A/'epoch_durable_neural_checkpoint_CPU32_preflight_v2_20261007/verification.json'),
      'new_CPU20_streamed_native_fits_completed_and_positive_model_score_direction_observed':True,
      'larger_GPU_direction_and_other_deferred_families_not_globally_exhausted':True,'global_optimization_boundary_proven':False,
      'fixed_user_stop_at_local':'2026-10-07T23:55:00+08:00','automatic_morning_restart_enabled':False,
      'input_sha256':{str(p):sha(p) for p in sources},'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
