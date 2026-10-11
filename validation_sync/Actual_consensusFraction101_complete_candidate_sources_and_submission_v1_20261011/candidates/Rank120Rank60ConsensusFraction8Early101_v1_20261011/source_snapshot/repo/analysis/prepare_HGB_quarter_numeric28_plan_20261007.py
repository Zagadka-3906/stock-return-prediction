"""Predeclare remaining numerical paths, with no test labels and no new scores."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    service=A/'service_owned_workflows_20261006/HGB_quarter_grid_numerical_coverage_audit'
    assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='passed'
    proof_path=A/'HGB_quarter_grid_numerical_coverage_20261007/verification.json';proof=read(proof_path)
    assert len(proof['raw_controls'])==7 and len(proof['forecast_controls'])==84
    distinct=proof['distinct_numerical_validation_paths_requiring_future_official_comparison'];assert len(distinct)==24
    previous_path=A/'flagged_HGB_weighted_quarters340_plan_20261007.json';previous=read(previous_path)
    counts={tuple(r['quarter_counts']) for r in distinct};assert len(counts)==2
    ensembles={}
    for coefficient in sorted(counts):
        names=[h for h,count in zip(previous['single_native_heads'],coefficient) for _ in range(count)]
        assert len(names)==4 and len(set(names))==2
        name='ordered_quarters_'+'_'.join(map(str,coefficient));ensembles[name]=names
        assert {r['weight'] for r in distinct if tuple(r['quarter_counts'])==coefficient}==set(previous['weights'])
    plan=A/'HGB_quarter_numeric28_plan_20261007.json';assert not plan.exists()
    create(plan,{'status':'predeclared24_distinct_numeric_variants_plus3_qualified_anchors_and_ablation_unscored',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'planned_round':118,'planned_wave':401,'preceding_round':117,
      'qualified_anchor_rounds':[112,116,117],'single_native_heads':previous['single_native_heads'],
      'ensembles':ensembles,'weights':previous['weights'],'universe':previous['universe'],
      'existing_native_bank':previous['existing_native_bank'],'new_native_fits':0,'existing_native_fits':20,
      'expected_scored_records':28,'nonanchor_records':25,'weighted_nonanchor_records':24,
      'actual_numerical_coverage_source':str(proof_path),'omitted_old35_grid_numeric_paths_requiring_fresh_official_scores':24,
      'native_storage_unique_components':True,'actual_comparison_parent_choice':'highest complete qualified112_116_117 original official S; exact tie earliest',
      'actual_scheme_base_choice':'highest compatible106 core complete qualified112_116_117 official S; exact tie earliest',
      'incompatible_qualified_anchors_remain_candidates':True,'fixed_reference_training_teacher_round':106,
      'explicit_ablation':'remove_flagged_HGB: preserve current complete nonflag parent and original106 flag forecasts',
      'aggregation':'float64 zero; add declared four repeated head slots in order; divide by four',
      'validation_required':'all25 full5635800 independentCDF and75 cold80_260_975; original official eight metrics for28 records',
      'freeze_then_full1599600_native_independent_two_replays_cold80_CSV_fullQA29_and_main_required':True,
      'exact_anchor_reuse_requires_all_validation_bits8_metrics_graph_all_bytes_original_freeze_and0new_inference':True,
      'complete118_pipeline_must_be_prepared_and_admitted_before_actual_official_scoring':True,
      'actual117_full_qualification_and_publisher_serialization_required':True,'new_quality_scores':0,
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),proof_path,previous_path]},
      'selection_bias_uncorrected':True,'global_exhaustion_not_established':True,'test_labels_read':False})
    print({'status':'predeclared','numeric_variants':24,'official_cases':28},flush=True)

if __name__=='__main__':main()
