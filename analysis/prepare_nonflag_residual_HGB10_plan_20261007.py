"""Predeclare a new nonflag teacher-residual family, without using any test outcomes."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
def main():
    p=A/'nonflag_residual_HGB10_plan_20261007.json';assert not p.exists()
    old=A/'cpu_full_universe_HGB_bank24_plan_20261007.json';original=read(old)
    configs={'nonflag_residual_hgb7_squared':{'loss':'squared_error','max_leaf_nodes':7},
             'nonflag_residual_hgb15_absolute':{'loss':'absolute_error','max_leaf_nodes':15}}
    create(p,{'status':'predeclared_unfitted10_nonflag_teacher_residual_HGB_models','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'configurations':configs,'fixed_parameters':original['fixed_parameters'],'CPU_threads':4,
      'native_fit_years':[2021,2022,2023,2024,2025],'prospective_native_fits':10,
      'training_population':'only existing 2020-2024 expanding OOF keys with flag_limit_up!=1, price_valid and finite original rank label',
      'teacher_round':106,'teacher':'same-day qualified106 expanding OOF forecast average_rank/N over all rows including sentinels',
      'features':'63 supplied-field-derived features plus teacher current forecast percentile,64 total',
      'target':'past mature original y_rank+0.5 minus same-row teacher percentile',
      'first2020':'zero residual because no earlier OOF teacher training keys available',
      'preprocessing':'each feature finite median then mean/std calculated columnwise on corresponding mature train rows;clip10; no full-validation fit',
      'feature_cache':'E:/赛题五_本机临时/nonflag_residual_HGB10_20261007, bounded eight-feature joins and8192-row mature window extraction',
      'new_family_difference':'prior full63-feature HGB used direct y_rank or return labels over original pre-2020 history; prior64-feature teacher-residual HGB restricted to flagged rows. This family fits nonflag residuals on past expanding OOF rows.',
      'later_planned_round':120,'later_anchor_rounds':[112,118,119],
      'later_heads':['nonflag_residual_hgb7_squared','nonflag_residual_hgb15_absolute','equal_mean_two'],
      'later_weights':[.0003125,.000625,.00125,.0025,.005,.0075,.01,.015,.02,.03,.04,.05],
      'later_expected_official_records':40,'later_requirement':'full37 independent current-day CDF transforms and111 cold controls;40 full official scores;freeze;complete selected native and independent future1599600/two replays/cold80/CSV;fullQA31/all-source parameters/main',
      'later_transform':'replace nonflag outputs with106 current percentile plus weighted predicted residual through106 current empirical inverseCDF; retain complete selected-parent flag raw bits; first2020 identity',
      'official_scoring_not_authorized_by_plan_without_complete_round120_source_admission':True,
      'early_stopping':False,'test_labels_read':False,'new_quality_scores':0,'all_training_validation_years_previously_viewed':True,
      'selection_bias_uncorrected':True,'global_direction_or_resource_exhaustion_not_established':True,
      'input_sha256':{str(s):sha(s) for s in [Path(__file__),old,A/'cpu_conditional_residual_hgb_bank20_plan_20261007.json',ROOT/'后续选模标准.md']}})
    print({'status':'predeclared','native_fits':10,'later_official_records':40},flush=True)
if __name__=='__main__':main()
