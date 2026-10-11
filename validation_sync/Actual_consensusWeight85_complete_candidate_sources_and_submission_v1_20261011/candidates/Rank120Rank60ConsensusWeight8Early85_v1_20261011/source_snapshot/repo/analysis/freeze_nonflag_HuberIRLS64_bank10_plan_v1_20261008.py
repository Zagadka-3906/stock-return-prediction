"""Freeze two fixed Huber recipes and five own-mature fits each before fitting or quality scoring."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    from nonflag_HuberIRLS64_streamed_v1_20261008 import CONFIGS
    paths=[Path(__file__),A/'train_nonflag_HuberIRLS64_bank10_v1_20261008.py',
        A/'nonflag_HuberIRLS64_streamed_v1_20261008.py',A/'nonflag_HuberIRLS64_own_window_v1_20261008.py',
        A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'memory_bounded_numeric_preparation_20261007.py',
        A/'nonflag_residual_Ridge_codec_20261007.py',A/'actual_nonflag_HuberIRLS64_small_location_v2_20261008.json']
    create(A/'nonflag_HuberIRLS64_bank10_plan_v1_20261008.json',{'status':'frozen_before_actual10_own_mature_fits_and_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},'configurations':CONFIGS,
        'native_fit_years':list(range(2021,2026)),'actual_declared_native_fits':10,'target':'provided_y_rank_plus_half_minus_teacher106_daily_average_rank_over_all_N',
        'universe':'valid_nonflag_finite_provided_train_target','training_preprocessing':'reused_only_from_identical_own_mature_verified_window',
        'purge_days':1,'validation_years':list(range(2020,2025)),'first2020_identity_residual':True,'CPU_threads':2,
        'out':'E:/赛题五_本机临时/nonflag_HuberIRLS64_bank10_v1_20261008','future_X_and_Y_read':False,'actual_official_scores':0,
        'actual200k_dense_native_control_required_before_full_fits':True,'no_validation_early_stop_or_target_clipping':True,
        'selected_candidate_and_complete_parent_pipeline_required_before_quality_admission':True,
        'finite_recipe_not_global_optimization_boundary':True})


if __name__=='__main__':main()
