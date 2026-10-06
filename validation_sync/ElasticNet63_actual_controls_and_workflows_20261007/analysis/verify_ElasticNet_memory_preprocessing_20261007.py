"""Actual historical63-field preprocessing semantic and dense training layout control."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import numpy as np,polars as pl
    import cpu_conditional_residual_mlp_codec_20261007 as reference
    import ElasticNet_memory_bounded_preprocessing_20261007 as bounded
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    from run import fold_cutoff
    out=A/'ElasticNet_memory_preprocessing_preflight_20261007';assert not out.exists();out.mkdir()
    files=[Path(__file__),A/'ElasticNet_memory_bounded_preprocessing_20261007.py',A/'cpu_conditional_residual_mlp_codec_20261007.py',ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',ROOT/'run.py'];pins={str(p.resolve()):sha(p) for p in files}
    create(out/'frozen_before_actual_control.json',{'input_sha256':pins,'new_fits':0,'new_official_scores':0})
    with LockedReadHashCache(pins) as scope:
        features=read(ROOT/'data/feature_manifest.json')['features'];frame=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('trade_date')<fold_cutoff(2020))).select(features).head(4097).collect();x=frame.to_numpy().astype(np.float64)
        controls=[]
        for values in [x,np.concatenate([x,np.full((1,63),np.nan)],axis=0)]:
            a=reference.fit_preprocessing(values);b=bounded.fit_preprocessing(values)
            for key in ('median','mean','scale'):assert np.allclose(a[key],b[key],rtol=1e-12,atol=1e-12),key
            actual=bounded.prepare_training_fortran(values,b);expected=reference.prepare(values,b)
            assert actual.flags.f_contiguous and np.array_equal(actual.view('u8'),expected.view('u8'))
            controls.append({'actual_rows':len(values),'column_temporary_statistics_semantically_equal_to_reference_1e_minus12':True,'actual_Fortran_training_matrix_bits_equal_to_prediction_preparation_same_statistics':True})
        scope.reverify();create(out/'verification.json',{'status':'passed_actual_historical63_column_statistics_and_native_training_layout_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'controls':controls,'new_fits':0,'new_official_scores':0,'global_peak_RAM_or_whole_goal_speedup_not_claimed':True,'test_labels_read':False})
if __name__=='__main__':main()
