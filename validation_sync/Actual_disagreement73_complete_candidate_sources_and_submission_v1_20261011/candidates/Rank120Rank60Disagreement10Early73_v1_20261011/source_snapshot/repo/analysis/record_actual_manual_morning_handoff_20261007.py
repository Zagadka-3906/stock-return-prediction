"""Write a truthful durable handoff; no automatic dispatch after tonight's fixed stop."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    output=A/'actual_manual_morning_optimization_handoff_20261007.json';assert not output.exists()
    rounds=[];best=None
    for number in range(127,132):
        full=A/f'optimization_20261003_r{number}/full_registration_execution.json';receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        qualified=full.exists() and receipt.exists() and read(full)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        row={'round':number,'actual_full_board_and_main_closed':qualified}
        if qualified:
            row.update(main_receipt=read(receipt),selection_metrics=read(A/f'optimization_20261003_r{number}/selection.json')['winner']['metrics'])
            if best is None or row['selection_metrics']['final_score']>best['selection_metrics']['final_score']:best=row
        rounds.append(row)
    sparse=A/'nonflag_SparseGram64_actual_native3_full37_cold111_controls_20261007.json'
    assert read(sparse)['status']=='passed_actual_sparse_native3_full37_independent_CDF_and111_cold_controls'
    deferred=A/'nonflag_ReverseBayes40_round132_dispatch_deferred_until_manual_continue_20261007.json';assert read(deferred)['official_scores_added']==0
    sources=[Path(__file__),sparse,deferred,A/'nonflag_residual_SparseGram64_bank10_20261007/verification.json',
      A/'manual_next_run_GPU_speed_and_epoch_checkpoint_bench_plan_20261007.json',A/'actual_GPU_shared_allocation_resource_boundary_20261007.json',
      A/'actual_two_process_scoring_latency_interpretation_20261007.json',A/'sparse_main_API_transport_recovery_20261007/receipt.json',
      A/'actual_GPU_shared_memory_and_manual_bench_plan_github_recovery_v4_20261007/receipt.json']
    create(output,{'status':'durable_manual_resume_handoff_not_automatic_restart_or_global_goal_completion',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'stop_at_local':'2026-10-07T23:55:00+08:00',
      'actual_user_continue_required_next_morning':True,'automatic_restart_enabled':False,'global_optimization_boundary_proven':False,
      'best_fully_qualified_at_handoff':best,'rounds':rounds,'input_sha256':{str(p):sha(p) for p in sources},
      'remaining_actions_in_priority_order':[
        {'direction':'finish_unclosed131_if_any','condition':'only if full source/browsers/main closure is missing after shutdown; preserve already executed40 scores and new candidate inference, do not rerun as new quality records'},
        {'direction':'ReverseBayes40','condition':'fresh manual dispatch with current actual131 parent and source gate; original mathematical sources/native10 and3/37/111 controls preserved; expired20261007 cutoff queue cannot be reused as automatic authorization'},
        {'direction':'SparseGram64_L1_Elastic_complete40','actual_mature_models_ready':10,'actual_native_hook_controls_ready':3,'actual_full_transform_controls_ready':37,'actual_cold_prefix_controls_ready':111,
         'condition':'prepare and admit complete source schema, actual qualified-parent comparisons, whole frozen scheme, return calibration, two full native/independent future replays, cold80 and all original ranking QA before qualification',
         'official_sparse_scores_added_today':0,'proposed_heads':['nonflag_residual_sparseGram64_L1','nonflag_residual_sparseGram64_Elastic','ordered_equal_mean_two'],
         'proposed_weights':[.0003125,.000625,.00125,.0025,.005,.0075,.01,.015,.02,.03,.04,.05]},
        {'direction':'GPU_memory_and_epoch_checkpoint_bench','condition':'first verify current free GPU and actual tiny GPU checkpoint continuation, then benchmark micro8192/accum4, BF16 or TF32 as distinct scientific recipes; preserve completed2020/2021 original native files',
         'current_original_fit_has_no_intra_annual_checkpoint':True,'unsaved2022_cannot_survive_poweroff':True,'GPU_new_recipe_speed_or_equivalence_not_yet_proven':True},
        {'direction':'cross_family_residual_ensembles','condition':'predeclare whole final graph and independent decoder for ordered Ridge/RFF/Bayes/sparse mixtures; 0 extra fits possible but still need all official scores/candidate controls before adoption'},
        {'direction':'two_process_official_scoring_admission','condition':'historical uncached4/serial4 equality is proven; isolate completed shared cache donors and reservations before applying concurrency to future official search; current wall ratio is workload-dependent'}],
      'source_and_model_cleanup':'do not delete candidate/bank files referenced by live or next-run pins; current data/model/temp remain on D/E',
      'best_parameters_not_automatically_promoted_to_active_release':True,'selection_bias_uncorrected':True,'test_labels_read':False})
    print('Written durable manual handoff; current qualified best round='+str(best['round']),flush=True)

if __name__=='__main__':main()
