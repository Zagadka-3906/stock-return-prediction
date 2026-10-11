"""Freeze a new20-fit Huber grid and wait for preceding47 candidate to finish."""
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service


def main():
    sources=[Path(__file__),A/'train_lowalpha_huber_residual_bank20_20261006.py',
        A/'train_robust_conditional_residual_bank20_20261006.py',
        A/'train_conditional_flag_residual_bank_20261006.py',
        A/'conditional_identity_regression_tree_codec_20261006.py',
        A/'conditional_residual128_256_bank40_20261006/verification.json',
        ROOT/'后续选模标准.md']
    for p in sources:
        if p.suffix=='.py':compile(p.read_text(encoding='utf-8'),str(p),'exec')
    pins={str(p):sha(p) for p in sources}
    frozen=A/'lowalpha_huber_residual20_frozen_hidden_admission_20261006.json'
    state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
    originals={name:row for name,row in state['activated_jobs'].items() if owned(row)}
    wide=read(A/'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
    if owned(wide):originals['neural16384_annual']=wide
    create(frozen,{'status':'frozen_before_actual20_fresh_lowalpha_Huber_native_fits',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'fixed_absolute_gradient_thresholds':[.05,.1],'objective':'huber',
        'feature_sets':['rank_only','provided63_plus_parent95_percentile'],
        'matched_L2_rounds':128,'num_leaves':7,'annual_years':[2021,2022,2023,2024],
        'final_training_year':2025,'expected_actual_native_fits':20,
        'all_new_fits_no_partial_recovery_fit_reused':True,
        'all_matching_mature_targets_features_windows_other_parameters_and_independent_codec_required':True,
        'full_comparison_freeze_inference_ranking_and_main_publication_still_required':True,
        'original_live_scientific_workers_preserved':originals,
        'scientific_workers_stopped_or_restarted':0,'test_labels_read':False})
    pins[str(frozen)]=sha(frozen)
    row=start_service('lowalpha_huber_residual_native_bank20',
        'train_lowalpha_huber_residual_bank20_20261006.py',[],pins)
    create(A/'lowalpha_huber_residual20_hidden_launch_20261006.json',{
        'status':'passed_actual_hidden_owned20_fit_admission_awaiting_real47_candidate_seal',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'identity':row,'input_sha256':pins,
        'actual_native_console_handle':row['actual_native_console_handle'],
        'actual_training_or_scores_not_claimed_complete':True,
        'original_scientific_workers_stopped_or_restarted':0,'test_labels_read':False})
    print('Fresh20-model low-alpha Huber bank admitted after real47 candidate seal.',flush=True)


if __name__=='__main__':main()
