"""Verify scoped SHA reuse on actual mature model reuse andfuture prefixes."""
from pathlib import Path
import gc
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from locked_read_hash_cache_20261004 import LockedReadHashCache,fresh_sha
OUT=ROOT/'analysis/locked_no_dropout_model_reuse_preflight_20261004'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2)

def main():
    OUT.mkdir(exist_ok=True)
    if (OUT/'verification.json').exists():
        for p,d in read(OUT/'verification.json')['input_sha256'].items():assert fresh_sha(p)==d,p
        print('Frozen locked model reuse controls verified');return
    import numpy as np
    import polars as pl
    import no_dropout_seed_model_sources_20261004 as router
    basis=ROOT/'analysis/locked_ensemble_provenance_preflight_20261004'
    proof=read(basis/'verification.json');assert proof['status']=='passed'
    future=ROOT/'analysis/no_dropout_seed_future_models_qa_20261004'
    full=read(future/'verification.json');assert full['status']=='passed'
    expected=read(basis/'actual_validated_hash_inputs.json')['input_sha256']
    infos={name:read(router.source_dir(name)/'info_2025.json') for name in router.NEW_CONFIGS}
    full_records={r['model']:r for r in full['native_models']}
    sources=[Path(__file__),ROOT/'analysis/locked_read_hash_cache_20261004.py',basis/'verification.json',
        basis/'actual_validated_hash_inputs.json',future/'verification.json']
    for name in router.NEW_CONFIGS:
        info_path=router.source_dir(name)/'info_2025.json';model=router.model_path(name,2025)
        assert infos[name]['status']=='passed' and infos[name]['model_sha256']==fresh_sha(model)
        expected[str(model.resolve())]=infos[name]['model_sha256']
        expected[str(info_path.resolve())]=fresh_sha(info_path)
        sources.extend((info_path,model,future/(name+'_raw.parquet')))
    modules=[]
    for name,module in sorted(sys.modules.copy().items()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().parent==ROOT/'analysis' and callable(getattr(module,'sha',None)):
            modules.append((name,module,module.sha));sources.append(Path(file))
    sources=list(dict.fromkeys(sources));hashes={str(p.resolve()):fresh_sha(p) for p in sources}
    write(OUT/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':hashes,'locked_immutable_input_sha256':expected,'models':list(router.NEW_CONFIGS),
        'actual_future_prefix_days':2,'new_quality_scores':0,'actual_new_fits_allowed':0,
        'live_queued_sources_changed':False,'test_labels_read':False})
    engine=router.native.engine;features=engine.feature_names()
    lazy=pl.scan_parquet(engine.FEATURE_FILE)
    days=lazy.filter(~pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_list()[:2]
    frame=lazy.filter(~pl.col('is_train')&pl.col('trade_date').is_in(days)).select(engine.KEYS+features+['price_valid']).sort('trade_date','ts_code').collect()
    assert len(frame)==9300 and frame['trade_date'].n_unique()==2
    x=engine.to_matrix(frame,features);dates=frame['trade_date'].to_numpy();valid=frame['price_valid'].to_numpy()
    outputs={};baseline=[]
    for name in router.NEW_CONFIGS:
        start=time.perf_counter();assert router.train_one(name,2025)==infos[name]
        pred=router.predict_arrays(router.load_bundle(router.model_path(name,2025)),x,dates=dates,valid=valid)
        pred[~valid]=-1e6
        raw=pl.read_parquet(future/(name+'_raw.parquet')).head(len(frame))
        assert raw.select(engine.KEYS).equals(frame.select(engine.KEYS))
        assert np.array_equal(pred,raw['pred_raw'].to_numpy()),name
        outputs[name]=pred;baseline.append({'model':name,'seconds':time.perf_counter()-start});gc.collect()
        print('Original mature model reuse andfuture prefix passed: '+name,flush=True)
    cached=[];start=time.perf_counter()
    with LockedReadHashCache(expected) as cache:
        try:
            for _,module,_ in modules:module.sha=cache.sha
            for name in router.NEW_CONFIGS:
                begin=time.perf_counter();assert router.train_one(name,2025)==infos[name]
                pred=router.predict_arrays(router.load_bundle(router.model_path(name,2025)),x,dates=dates,valid=valid)
                pred[~valid]=-1e6
                assert np.array_equal(pred,outputs[name]),name
                cached.append({'model':name,'seconds':time.perf_counter()-begin});gc.collect()
                print('Locked mature model reuse andfuture prefix passed: '+name,flush=True)
        finally:
            for _,module,original in modules:module.sha=original
        hits=cache.hits;fallback=cache.fresh_calls
    total=time.perf_counter()-start
    assert all(module.sha is original for _,module,original in modules)
    for p,d in hashes.items():assert fresh_sha(p)==d,p
    assert len(list(router.native.OUT.glob('*/info_2025.json')))==4
    assert len(list(router.virtual.OUT.glob('*/info_2025.json')))==4
    write(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'all8_existing_mature_model_infos_exact':True,'actual_new_fulltraining_fits':0,
        'all8_actual_future9300_row_complete_day_prefix_bit_identical':True,
        'existing_full_future_raw_prefix_bit_identical':True,'all_actual_model_andraw_artifacts_unchanged':True,
        'models':list(router.NEW_CONFIGS),'rows':len(frame),'days':2,'baseline_model_checks':baseline,
        'cached_model_checks':cached,'cached_complete_seconds_including_setup_andexit':total,
        'cache_hits':hits,'nonsealed_paths_rehashed':fallback,'original_namespace_restored':True,
        'background_andfilesystem_cache_not_matched':True,'adopted_in_live_queued_rounds':False,
        'scope':'Actual artifact-reuse branches andtwo complete future days only; full scheme scoring andcalibration remain separate. No complete official score claimed.',
        'new_quality_scores':0,'test_labels_read':False,'input_sha256':hashes})
    print('All8 actual model-reuse andfuture-prefix controls passed',flush=True)

if __name__=='__main__':main()
