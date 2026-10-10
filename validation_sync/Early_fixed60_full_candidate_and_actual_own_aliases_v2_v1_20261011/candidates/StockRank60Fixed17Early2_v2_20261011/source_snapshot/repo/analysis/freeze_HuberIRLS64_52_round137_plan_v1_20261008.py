"""Freeze48 signed-Huber CDF cases, one identity and three complete qualified anchors."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    cases=[{'group':group,'amplitude':weight} for group in range(6) for weight in (.0025,.005,.01,.025,.05,.075,.1,.2)]
    paths=[Path(__file__),A/'HuberIRLS64_complete_parent_CDF_v1_20261008.py',A/'HuberIRLS64_complete_parent_native_stage_v1_20261008.py',
        A/'predict_HuberIRLS64_complete_parent_scheme_v1_20261008.py',A/'nonflag_HuberIRLS64_bank10_plan_v1_20261008.json',
        A/'CrossFamily_complete_parent_CDF_v1_20261008.py',A/'predict_CrossFamily_complete_parent_scheme_v1_20261008.py',
        A/'predict_BF16_complete_parent_rank_scheme_v1_20261008.py',A/'predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py']
    create(A/'HuberIRLS64_52_round137_plan_v1_20261008.json',{'status':'frozen52_case_grid_before_any_Huber_quality_score',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':137,'input_sha256':{str(p):sha(p) for p in paths},
        'new_cases':cases,'new_case_count':48,'anchors':[134,135,136],'identity_cases':1,'total_cases':52,
        'comparison_parent':'highest_official_S_among_fully_qualified134135136_after136_QA47_and_main',
        'complete_parent_preserves_signed_Bayes_optional_BF16_and_CrossFamily':True,'full_validation_rows':5635800,
        'validation_years':list(range(2020,2025)),'actual_candidate_rows':1599600,'tie_order':['score_desc','unique_physical_native_models','amplitude','case'],
        'quality_admission_requires':'actual10_model_bank_actual49_full_CDF147cold_actual18_historical_native_hooks_and_complete52_receiver_route_preflight',
        'candidate_admission_requires':'full_graph_source_bytes_return_mapping_freeze_and_two_full_native_independent_replays_and_cold80_or_exact_anchor_reuse',
        'full_round_requires':'original_official_all8_metrics_all6views45second_QA48_complete_board_and_remote_main_receipt',
        'new_quality_scores':0,'future_X_and_Y_read':False,'future_wrapper_not_yet_actual_candidate_qualified':True,
        'negative_BF16_new_bank_direction_still_uncovered':True,'finite_grid_not_global_exhaustion':True})


if __name__=='__main__':main()
