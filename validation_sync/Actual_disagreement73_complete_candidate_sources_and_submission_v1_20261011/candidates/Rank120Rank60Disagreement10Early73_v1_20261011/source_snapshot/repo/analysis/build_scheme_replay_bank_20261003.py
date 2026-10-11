"""Frozen raw/role-ready OOF inputs for replaying every layer of a complete scheme."""
from pathlib import Path
import sys
import time
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import polars as pl
import linear_model_sources_20261003 as models
from optimize_training_round18 import YEARS,KEYS,BASE_POST,read,dump,sha,log
from src.scoring import Panel
from optimize_wave6 import make_prediction_param
OUT=ROOT/'analysis/complete_scheme_replay_20261003'
FRAME=ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet'


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    OUT.mkdir(exist_ok=True)
    if (OUT/'protocol.json').exists():verify();return
    models.verify()
    sources=[Path(__file__),Path(models.__file__),FRAME,
             ROOT/'analysis/optimize_training_round18.py',ROOT/'src/scoring.py',
             ROOT/'analysis/connected_validation_20261002/optimize_wave6.py',ROOT/'src/postprocessing.py',
             ROOT/'analysis/preflight_complete_scheme_replay_20261003.py',
             ROOT/'analysis/complete_scheme_replay_preflight_20261003/verification.json']
    assert read(sources[-1])['status']=='passed'
    for name in models.CONFIGS:
        for year in YEARS:
            sources.extend(models.source_dir(name)/f'{kind}_{year}.{suffix}'
                           for kind,suffix in (('model','joblib'),('raw','parquet'),('info','json')))
    qa=ROOT/'analysis/complete_scheme_replay_preflight_20261003'
    sources.extend((qa/'rankers').glob('*.npy'))
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'models':list(models.CONFIGS),'years':YEARS,'rows':5635800,'days':1212,
         'raw_inputs':'Verified full annual OOF raw predictions, sorted and key-matched to identical validation dates.',
         'role_inputs':'Per-fold make_prediction_param using only keys, price validity, limit flags, current auxiliary signal and raw predictions; label column set to null. alpha=0 and bonus=0 match earlier role augmentation arrays.',
         'role_postprocessing':dict(BASE_POST,alpha=0,bonus=0),
         'new_training_runs':0,'new_model_scores':0,'test_data_read':False,
         'input_sha256':{str(path.resolve()):sha(path) for path in dict.fromkeys(sources)}},immutable=True)


def main():
    freeze()
    if (OUT/'oof_audit.json').exists():
        audit=read(OUT/'oof_audit.json')
        for path,digest in audit['output_sha256'].items():assert sha(path)==digest,path
        return
    for folder in ('raw','rankers'):(OUT/folder).mkdir(exist_ok=True)
    # Select no old model columns; no target values enter either output transform.
    frame=pl.read_parquet(FRAME).select(KEYS+['flag_limit_up','price_valid','aux_raw'])
    frame=frame.with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    parts={year:frame.filter(pl.col('trade_date')//10000==year) for year in YEARS}
    proofs=[];outputs={}
    for name in models.CONFIGS:
        raw_parts=[];role_parts=[]
        for year in YEARS:
            source=models.source_dir(name);info=read(source/f'info_{year}.json')
            meta=info['training_meta'];assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
            path=source/f'raw_{year}.parquet';assert sha(path)==info['prediction_sha256'] and info['model_reload_bit_identical']
            raw=pl.read_parquet(path);fold=parts[year];assert raw.select(KEYS).equals(fold.select(KEYS))
            values=raw['pred_raw'].to_numpy();assert np.isfinite(values).all()
            raw_parts.append(values)
            role_parts.append(make_prediction_param(Panel.from_frame(fold.with_columns(pl.Series('pred_raw',values))),
                              fold['aux_raw'].to_numpy(),**dict(BASE_POST,alpha=0,bonus=0)))
        paths=[OUT/f'raw/{name}.npy',OUT/f'rankers/{name}.npy']
        arrays=[np.concatenate(raw_parts),np.concatenate(role_parts)]
        for path,values in zip(paths,arrays):
            if path.exists():assert np.array_equal(np.load(path),values),path
            else:np.save(path,values)
            outputs[str(path.resolve())]=sha(path)
        control=ROOT/f'analysis/complete_scheme_replay_preflight_20261003/rankers/{name}.npy'
        old_match=None
        if control.exists():
            assert np.array_equal(arrays[1],np.load(control)),name;old_match=True
        proofs.append({'model':name,'annual_folds':5,'rows':len(arrays[0]),'old_active_role_array_bit_identical':old_match})
        log(f'Replay OOF bank {name} completed ({len(proofs)}/{len(models.CONFIGS)})')
    dump(OUT/'oof_audit.json',{'status':'passed','controls':proofs,'new_training_runs':0,
         'new_model_scores':0,'test_data_read':False,'label_columns_removed_before_processing':True,
         'output_sha256':outputs},immutable=True)
    log('All complete-scheme replay inputs verified; no new model scores generated')


if __name__=='__main__':main()
