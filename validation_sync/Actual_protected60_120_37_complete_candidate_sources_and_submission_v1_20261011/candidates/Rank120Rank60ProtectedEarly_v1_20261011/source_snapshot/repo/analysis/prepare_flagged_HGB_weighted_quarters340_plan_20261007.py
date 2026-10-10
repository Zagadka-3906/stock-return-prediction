"""Predeclare uncovered ordered quarter mixtures, without reading new scores or future X."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def canonical(names,heads):
    return tuple(Fraction(names.count(head),len(names)) for head in heads)

def main():
    old_path=A/'flagged_HGB_small_amplitude88_plan_20261007.json';old=read(old_path)
    heads=old['single_native_heads'];assert len(heads)==4
    old_groups=[[n] for n in heads]+list(old['ensembles'].values())
    covered={canonical(group,heads) for group in old_groups};assert len(covered)==7
    ensembles={};counts={};already=[]
    for coefficient in product(range(5),repeat=4):
        if sum(coefficient)!=4:continue
        ordered=[head for head,count in zip(heads,coefficient) for _ in range(count)]
        if canonical(ordered,heads) in covered:
            already.append(coefficient);continue
        name='ordered_quarters_'+'_'.join(map(str,coefficient))
        ensembles[name]=ordered;counts[name]=list(coefficient)
        assert 2<=len(set(ordered))<=3 and len(ordered)==4
    assert len(ensembles)==28 and len(already)==7
    plan=A/'flagged_HGB_weighted_quarters340_plan_20261007.json';assert not plan.exists()
    create(plan,{'status':'predeclared_unscored_uncovered_flagged_HGB_ordered_quarter_grid',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'planned_round':117,'planned_wave':400,'preceding_round':116,
        'qualified_anchor_rounds':[112,115,116],
        'actual_comparison_parent_choice':'highest complete qualified112_115_116 official S; exact tie earliest',
        'actual_scheme_base_choice':'highest complete qualified112_115_116 compatible106_core_plus_optional_flag_HGB_lower_pool; exact tie earliest',
        'incompatible_qualified_anchors_remain_candidates':True,'fixed_reference_training_teacher_round':106,
        'single_native_heads':heads,'ensembles':ensembles,'quarter_counts':counts,'weights':old['weights'],
        'universe':old['universe'],'new_nonanchor_mixtures':28,'weighted_nonanchor_records':336,
        'explicit_ablation':'remove_flagged_HGB: retain complete nonflag parent and original106 flag forecasts',
        'nonanchor_records':337,'expected_scored_records':340,
        'aggregation':'start float64 zeros; add heads in declared repeated order; divide by four; apply the original flag residual CDF with unchanged106 feature teacher',
        'existing_native_bank':old['existing_native_bank'],'existing_native_fits':20,'new_native_fits':0,
        'inference_native_components_unique_by_head_and_SHA':True,
        'ordered_aggregation_can_repeat_a_head_but_storage_reload_controls_and_native_fit_counts_must_not':True,
        'omitted_previously_covered_count_vectors':[list(c) for c in already],
        'coverage_evidence':'35 nonnegative four-head count vectors summing4; omit seven mixtures already covered by single heads and old equal means',
        'first2020_flag_branch_identity':True,'nonflag_complete_parent_output_bits_unchanged':True,
        'pool_and_transform_use_current_forecasts_flags_price_valid_only':True,
        'selection':'highest original official mapped2020_2024 full connected score; no extra single_metric worst_year or significance gate',
        'validation_required':'all337 full5635800 independentCDF and cold80_260_975; all340 original official eight metrics',
        'freeze_then_full1599600_native_independent_two_replays_cold80_CSV_and_full_QA28_main_required':True,
        'exact_anchor_reuse_requires_all_raw_validation_bits8_metrics_graph_parameters_bytes_original_freeze_and0new_inference':True,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old_path,A/'refine_flagged_HGB_compatible_parent_transform_20261007.py',
            A/'cpu_conditional_residual_hgb_bank20_20261007/verification.json',A/'cpu_HGB_large_batch20_benchmark_20261007/verification.json']},
        'selection_bias_uncorrected':True,'test_labels_read':False,'new_quality_scores':0,
        'future116_and117_full_qualification_not_claimed':True,'global_exhaustion_not_established':True})
    print({'status':'predeclared','new_ordered_mixtures':28,'official_cases':340,'new_fits':0},flush=True)

if __name__=='__main__':main()
