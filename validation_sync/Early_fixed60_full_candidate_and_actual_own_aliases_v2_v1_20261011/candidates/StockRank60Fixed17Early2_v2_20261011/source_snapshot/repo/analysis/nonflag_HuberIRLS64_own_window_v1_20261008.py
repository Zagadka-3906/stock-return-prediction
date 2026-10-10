"""Read-only admission of the existing teacher106 residual training windows."""
from pathlib import Path
import hashlib, json, os, sys
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
BANK=A/'nonflag_residual_HGB_bank10_20261007'
EBASE=Path('E:/赛题五_本机临时')


def numeric_sha(value):
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()


def atomic(path,value):
    path=Path(path); assert path.resolve().is_relative_to(EBASE.resolve()) and path.suffix=='.json'
    temporary=path.with_name(path.name+f'.part-{os.getpid()}')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(path)


def input_paths(years):
    alignment=read(BANK/'actual_teacher_target_and_key_alignment.json')
    cache=Path(alignment['feature_cache']).parent
    paths=[Path(__file__),A/'nonflag_HuberIRLS64_streamed_v1_20261008.py',
        A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'memory_bounded_numeric_preparation_20261007.py',
        A/'nonflag_residual_Ridge_codec_20261007.py',A/'nonflag_RFF128_streamed_gram_fitter_20261007.py',
        BANK/'verification.json',BANK/'actual_teacher_target_and_key_alignment.json',Path(alignment['feature_cache']),
        A/'connected_validation_20261002/combined_fold_frame.parquet',ROOT/'data/features.parquet',
        ROOT/'data/feature_manifest.json',ROOT/'run.py',A/'optimization_20261003_r106/selected_validation.npy']
    for year in years:
        info_path=BANK/'nonflag_residual_hgb7_squared'/f'info_{year}.json'
        info=read(info_path); assert sha(info['native_model_path'])==info['native_model_sha256']
        paths.extend((info_path,Path(info['native_model_path']),cache/f'mature_training_features64_{year}.npy'))
    return list(dict.fromkeys(paths))


def load_population():
    import gc,numpy as np,polars as pl
    frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',
        columns=['ts_code','trade_date','flag_limit_up','price_valid']).with_row_index('oof_position')
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    keys=frame.filter(pl.col('flag_limit_up')!=1)
    alignment=read(BANK/'actual_teacher_target_and_key_alignment.json')
    raw=np.load(alignment['feature_cache'],mmap_mode='r');assert raw.shape==(len(keys),64)
    assert numeric_sha(raw[:,63])==alignment['teacher_feature_numeric_sha256']
    teacher=np.load(A/'optimization_20261003_r106/selected_validation.npy',mmap_mode='r')
    dates=frame['trade_date'].to_numpy();positions=keys['oof_position'].to_numpy()
    pct=pl.DataFrame({'date':dates,'teacher':np.asarray(teacher)}).with_columns(
        (pl.col('teacher').rank(method='average').over('date')/pl.len().over('date')).alias('pct'))['pct'].to_numpy()
    assert np.array_equal(np.asarray(raw[:,63]).view('u8'),pct[positions].view('u8'))
    del teacher,pct
    labels=keys.select('ts_code','trade_date').join(pl.scan_parquet(ROOT/'data/features.parquet').filter(
        pl.col('is_train')&(pl.col('trade_date')>=20200101)).select('ts_code','trade_date','y_rank').collect(),
        on=['ts_code','trade_date'],how='left',validate='1:1',maintain_order='left')
    target=labels['y_rank'].to_numpy().astype(float)+.5-raw[:,63]
    assert numeric_sha(target)==alignment['target_numeric_sha256'];del labels;gc.collect()
    all_days=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')).select(
        'trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    return {'frame':frame,'raw':raw,'positions':positions,'dates':dates,'key_dates':keys['trade_date'].to_numpy(),
        'eligible':np.isfinite(target)&keys['price_valid'].to_numpy(),'target':target,'all_days':all_days,
        'alignment':alignment,'oof_days':np.unique(dates)}


def admitted_window(population,year):
    import numpy as np,joblib
    from run import fold_cutoff
    from nonflag_RFF128_streamed_gram_fitter_20261007 import prepared_sha
    info=read(BANK/'nonflag_residual_hgb7_squared'/f'info_{year}.json')
    cutoff=fold_cutoff(year);kd=population['key_dates'];indices=np.flatnonzero((kd<cutoff)&population['eligible'])
    last=int(kd[indices].max());end=int(population['all_days'][np.searchsorted(population['all_days'],last)+1])
    assert len(indices)==info['training_rows'] and last==info['last_training_label_date']
    assert end==info['last_training_label_end'] and end<=cutoff==info['exclusive_cutoff']
    window=np.load(Path(population['alignment']['feature_cache']).parent/f'mature_training_features64_{year}.npy',mmap_mode='r')
    assert window.shape==(len(indices),64)
    for left in range(0,len(indices),8192):
        value=population['raw'][indices[left:left+8192]]
        assert np.array_equal(window[left:left+len(value)].view('u8'),value.view('u8'))
    saved=joblib.load(info['native_model_path']);preprocessing=saved['preprocessing'];features=saved['features'];del saved
    target=population['target'][indices]
    assert prepared_sha(window,preprocessing)==info['training_matrix_numeric_sha256']
    assert numeric_sha(target)==info['training_target_numeric_sha256']
    assert len(features)==64 and features[-1]=='qualified106_current_forecast_average_rank_over_N'
    return window,target,preprocessing,features,info
