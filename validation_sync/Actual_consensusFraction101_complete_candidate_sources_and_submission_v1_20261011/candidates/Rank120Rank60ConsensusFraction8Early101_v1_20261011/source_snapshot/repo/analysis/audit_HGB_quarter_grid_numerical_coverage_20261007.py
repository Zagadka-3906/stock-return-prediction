"""Audit omitted proportional mixtures using actual full validation bits, never labels."""
from pathlib import Path
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def digest(v):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(v)).cast('B')).hexdigest()

def main():
    import numpy as np
    import polars as pl
    import psutil
    from refine_flagged_HGB_compatible_parent_transform_20261007 import prepare,apply_prepared
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    while psutil.virtual_memory().available<12*2**30:time.sleep(15)
    out=A/'HGB_quarter_grid_numerical_coverage_20261007';assert not out.exists();out.mkdir()
    plan_path=A/'flagged_HGB_weighted_quarters340_plan_20261007.json';plan=read(plan_path)
    old_path=A/'flagged_HGB_small_amplitude88_plan_20261007.json';old=read(old_path)
    old_scores=A/'flagged_HGB_small_amplitude88_official_comparison_v4_20261007/verification.json';records=read(old_scores)['records']
    bank=A/plan['existing_native_bank'];heads=plan['single_native_heads']
    parent_path=A/'optimization_20261003_r112/selected_validation.npy';ref_path=A/'optimization_20261003_r106/selected_validation.npy'
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    paths=[Path(__file__),plan_path,old_path,old_scores,parent_path,ref_path,frame_path,
      A/'refine_flagged_HGB_compatible_parent_transform_20261007.py',*[bank/h/'flagged_oof_predictions.npy' for h in heads]]
    pins={str(p):sha(p) for p in paths}
    create(out/'frozen_before_actual_numerical_audit.json',{'input_sha256':pins,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    groups={h:[h] for h in heads};groups.update(old['ensembles']);raw_controls=[];forecast_controls=[]
    with LockedReadHashCache(pins) as scope:
        frame=pl.read_parquet(frame_path,columns=['trade_date','ts_code','flag_limit_up','price_valid'])
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        parent=np.load(parent_path,mmap_mode='r');reference=np.load(ref_path,mmap_mode='r')
        arrays={h:np.load(bank/h/'flagged_oof_predictions.npy',mmap_mode='r') for h in heads}
        prepared=prepare(reference,dates,flags,valid,plan['universe'])
        for coefficient in plan['omitted_previously_covered_count_vectors']:
            ordered=[h for h,c in zip(heads,coefficient) for _ in range(c)]
            proportions=tuple(c/4 for c in coefficient)
            model=next(n for n,ns in groups.items() if tuple(ns.count(h)/len(ns) for h in heads)==proportions)
            ns=groups[model]
            if len(ns)==1:original=np.asarray(arrays[ns[0]])
            else:
                original=np.zeros(len(frame),dtype=np.float64)
                for h in ns:original+=arrays[h]
                original/=len(ns)
            repeated=np.zeros(len(frame),dtype=np.float64)
            for h in ordered:repeated+=arrays[h]
            repeated/=4.
            different=int(np.count_nonzero(original.view('u8')!=repeated.view('u8')))
            raw_controls.append({'quarter_counts':coefficient,'old_model':model,'raw_different_bits_rows':different,
              'original_raw_sha256':digest(original),'repeated_raw_sha256':digest(repeated)})
            for weight in plan['weights']:
                old_case=next(r for r in records if r['configuration']['model']==model and r['configuration']['weight']==weight)
                actual=apply_prepared(parent,reference,flags,original,weight,prepared)
                assert digest(actual)==old_case['prediction_numeric_bytes_sha256']
                variant=apply_prepared(parent,reference,flags,repeated,weight,prepared)
                count=int(np.count_nonzero(actual.view('u8')!=variant.view('u8')))
                forecast_controls.append({'quarter_counts':coefficient,'old_model':model,'weight':weight,
                  'actual_old88_case':old_case['case'],'actual_old_validation_sha256':digest(actual),
                  'quarter_validation_sha256':digest(variant),'different_full_forecast_bits_rows':count,
                  'may_reuse_all8_original_official_metrics_if_bits_identical':count==0,
                  'original_official_metrics':old_case['metrics'] if count==0 else None,
                  'not_scored_here':True,'future_candidate_not_inferred':True})
            print({'model':model,'raw_different_rows':different,'actual_completed_forecast_controls':len(forecast_controls)},flush=True)
        scope.reverify()
    assert len(raw_controls)==7 and len(forecast_controls)==84
    distinct=[r for r in forecast_controls if r['different_full_forecast_bits_rows']]
    create(out/'verification.json',{'status':'passed_actual7_omitted_raw_aggregations_and84_full5635800_forecast_comparisons_against_original88_bytes',
      'input_sha256':pins,'raw_controls':raw_controls,'forecast_controls':forecast_controls,
      'distinct_numerical_validation_paths_requiring_future_official_comparison':distinct,
      'actual_all35_mathematical_mixture_validation_numeric_coverage_established':not distinct,
      'future_inference_or_global_direction_exhaustion_not_claimed':True,
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'passed','raw_aggregation_controls':7,'full_forecast_controls':84,'distinct_unscored_forecast_paths':len(distinct)},flush=True)

if __name__=='__main__':main()
