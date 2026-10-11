"""Record measured WDDM shared allocation and predeclare manual next-run benchmarks."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    snapshot=A/'actual_neural_GPU_shared_memory_snapshot_20261007.json';sample=read(snapshot);row=sample['records'][0]
    launch=A/'service_owned_workflows_20261006/neural16384_annual/native_launch.json'
    assert sha(launch)==sample['native_launch_sha256'] and sample['worker_pid']==read(launch)['owned_worker_pid']
    info=A/'neural16384_full_bank_20261005/rank16384_drop000_seed07_e32/info_2021.json';actual=read(info);cfg=actual['configuration']
    width=len(actual['training_meta']['features']);count=0
    for h in cfg['hidden']:count+=(width+1)*h+2*h;width=h
    count+=width+1
    pins={str(p):sha(p) for p in [Path(__file__),snapshot,launch,info,A/'train_diverse_backbones_20261003.py',
      A/'epoch_durable_neural_checkpoint_adapter_v2_20261007.py',A/'epoch_durable_neural_checkpoint_CPU32_preflight_v2_20261007/verification.json']}
    create(A/'actual_GPU_shared_allocation_resource_boundary_20261007.json',{
      'status':'measured_original16384_recipe_uses_Windows_shared_GPU_allocation_on_this_host',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
      'GPU_process_dedicated_usage_GiB':row['DedicatedUsage']/2**30,'GPU_process_shared_usage_GiB':row['SharedUsage']/2**30,
      'GPU_process_TotalCommitted_GiB':row['TotalCommitted']/2**30,
      'provider_semantics':'Windows WDDM per-process memory allocation; not CUDA allocator peak, measured PCIe traffic or eviction count',
      'inference':'dedicated-plus-shared usage supports allocation beyond dedicated capacity; this can contribute to slow training but the causal time penalty was not benchmarked',
      'original_configuration':cfg,'actual_parameter_count_from_frozen_architecture':count,
      'analytic_FP32_parameter_storage_GiB':count*4/2**30,
      'analytic_FP32_parameter_plus_gradient_plus_two_Adam_state_storage_GiB':count*16/2**30,
      'analytic_one_copy_hidden_activation_storage_GiB':cfg['batch_size']*sum(cfg['hidden'])*4/2**30,
      'analytic_numbers_are_not_measured_total_allocator_peak':True,
      'completed2021_actual_fit_seconds':actual['fit_seconds'],
      'original_current_training_and_frozen_weights_not_modified':True,
      'global_feasible_direction_or_resource_exhaustion_not_established':True,'new_quality_scores':0,'test_labels_read':False})
    create(A/'manual_next_run_GPU_speed_and_epoch_checkpoint_bench_plan_20261007.json',{
      'status':'predeclared_manual_next_run_benchmarks_not_GPU_qualified_or_automatically_dispatched',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
      'actual_user_continue_required':True,'automatic_morning_restart_enabled':False,
      'timing_and_memory_benchmark_population':'bounded subset of verified own past mature 2021 training window; training only, no real future labels',
      'same_frozen_architecture':cfg['hidden'],'optimizer':'original AdamW parameters and fixed seed',
      'proposed_benchmark_recipes':[
        {'id':'FP32_micro8192_accum4','effective_batch_size':32768,'microbatch_size':8192,'optimizer_updates':'one per original outer batch, row-count-weighted loss accumulation','precision':'FP32, original TF32 disabled','new_scientific_floating_point_recipe':True},
        {'id':'BF16_micro8192_accum4','effective_batch_size':32768,'microbatch_size':8192,'precision':'GPU autocast BF16 if actually supported; FP32 parameters/optimizer','new_scientific_floating_point_recipe':True},
        {'id':'FP32_TF32_micro8192_accum4','effective_batch_size':32768,'microbatch_size':8192,'precision':'FP32 tensors with TF32 matmul explicitly enabled','new_scientific_floating_point_recipe':True}],
      'required_actual_controls':['record own input arrays, maturity and source hashes before each run','sample dedicated/shared WDDM memory and CUDA allocator peaks plus batch timing','reject nonfinite losses/weights','verify original-vs-epoch-durable GPU continuation across fresh processes','retain model, optimizer and CUDA RNG after every completed epoch on D or E','native reload and independent fixed-batch inference prefix controls before official candidate admission'],
      'FP32_32768_original_reference_may_exceed_free_dedicated_capacity_and_needs_admission_before_rebenchmark':True,
      'microbatch_accumulation_not_claimed_bit_identical_to_original_large_batch':True,
      'BF16_or_TF32_not_claimed_to_preserve_previous_FP32_model_weights':True,
      'CPU_checkpoint_equivalence_already_passed':True,'GPU_checkpoint_equivalence_not_yet_tested':True,
      'speedup_factor_not_measured_or_promised':True,'no_relabeling_or_partial_annual_weights_reuse_as_original_recipe':True,
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
